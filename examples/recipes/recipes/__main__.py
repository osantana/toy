import argparse

from prettyconf import config
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import create_database, database_exists, drop_database

from recipes.database import get_db
from recipes.models import User
from toy.server import HTTPServer

from .application import RecipesApp, get_app


def parse_host_port(hostname):
    host, port = hostname.rsplit(':', 1)
    return host, int(port)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='command')

    runserver = subparsers.add_parser('runserver', help='start server')
    runserver.set_defaults(command='runserver')
    runserver.add_argument('--hostname', metavar='hostname[:port]')

    initdb = subparsers.add_parser('initdb', help='create and initialize database')
    initdb.add_argument('--reset', action='store_true', help='will destroy your database and re-create it')
    initdb.set_defaults(command='initdb')

    adduser = subparsers.add_parser('adduser', help='add user')
    adduser.set_defaults(command='adduser')
    adduser.add_argument('--email', required=True)
    adduser.add_argument('--password', required=True)

    args = parser.parse_args()

    if args.command == 'runserver':
        hostname, port = config('HOSTNAME', default='127.0.0.1:8080', cast=parse_host_port)
        if args.hostname:
            hostname, port = parse_host_port(args.hostname)

        applicaton = get_app()
        server = HTTPServer(
            application=applicaton,
            hostname=hostname,
            port=port,
        )
        server.run()

    elif args.command == 'initdb':
        applicaton = RecipesApp()
        database_url = applicaton.config['database_url']

        if args.reset:
            drop_database(database_url)

        if not database_exists(database_url):
            create_database(database_url)

        db = get_db(applicaton)
        db.create_tables()

    elif args.command == 'adduser':
        application = get_app()
        db = application.extensions['db']

        user = User(
            email=args.email,
        )
        user.set_password(args.password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            print(f'User {user.email} already exists')
            return

        print(f'User {user.email} successfully created.')


if __name__ == '__main__':
    main()
