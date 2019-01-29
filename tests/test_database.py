from recipes.database import Database


def test_basic_database(database_url):
    db = Database()

    assert db.database_url is None
    assert db.engine is None
    assert db.connection is None


def test_database_init_db(application):
    db = Database()
    db.init_app(application)

    assert not db.connection.closed
