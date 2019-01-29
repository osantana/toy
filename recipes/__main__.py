import argparse

from prettyconf import config

from toy.server import HTTPServer
from .application import get_app


def parse_host_port(hostname):
    host, port = hostname.rsplit(':', 1)
    return host, int(port)


def main():
    parser = argparse.ArgumentParser()
    command = parser.add_mutually_exclusive_group()
    command.add_argument('--runserver', action='store_const', dest='command', const='runserver')
    command.add_argument('--initdb', action='store_const', dest='command', const='initdb')

    args = parser.parse_args()

    if args.command == 'runserver':
        hostname, port = config('HOSTNAME', default='localhost:8080', cast=parse_host_port)

        applicaton = get_app()
        server = HTTPServer(
            application=applicaton,
            hostname=hostname,
            port=port,
        )
        server.run()


if __name__ == '__main__':
    main()
