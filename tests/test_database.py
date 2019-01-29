from recipes.database import Database, get_db


def test_basic_database(database_url):
    db = Database()

    assert db.database_url is None
    assert db.engine is None
    assert db.connection is None


def test_database_init_db(application):
    db = Database()
    db.init_app(application)

    assert not db.connection.closed
    assert application.extensions['db'] == db


def test_database_get_db(application):
    get_db()
    assert 'db' not in application.extensions


def test_database_get_db_application_init(application):
    db = get_db(application=application)
    assert application.extensions['db'] == db


def test_database_singleton():
    db1 = Database.get()
    db2 = Database.get()

    assert db1 is db2
