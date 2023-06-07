from recipes.application import RecipesApp
from recipes.database import Database, get_db


def test_basic_database(database_url):
    db = Database()

    assert db.database_url is None
    assert db.engine is None
    assert db.connection is None


def test_database_init_db(create_test_db, database_url):
    app = RecipesApp(database_url=database_url)

    db = Database()
    db.init_app(app)

    assert not db.connection.closed
    assert app.extensions['db'] == db


def test_database_get_db():
    application = RecipesApp()
    db = get_db()
    assert db is not None
    assert 'db' not in application.extensions


def test_database_get_db_application_init(create_test_db, application):
    db = get_db(application=application)
    assert application.extensions['db'] == db


def test_database_singleton():
    db1 = Database.get()
    db2 = Database.get()

    assert db1 is db2