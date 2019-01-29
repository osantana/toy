from recipes.database import Database


def test_basic_database(connect_url):
    db = Database.get(connect_url)

    assert db.connect_url == connect_url
    assert not db.connection.closed


def test_database_singleton(connect_url):
    db1 = Database.get(connect_url)
    db2 = Database.get(connect_url)

    assert db1 is db2
