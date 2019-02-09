from datetime import timedelta

import pytest
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database, drop_database
from webtest import TestApp

from recipes.application import get_app
from recipes.models import Recipe


@pytest.fixture
def database_url():
    return 'postgresql://hellofresh:hellofresh@localhost/test_hellofresh'


@pytest.fixture
def create_test_db(database_url):
    try:
        drop_database(database_url)
    except ProgrammingError:
        pass

    create_database(database_url)
    yield
    drop_database(database_url)


@pytest.fixture
def database(create_test_db, application):
    db = application.extensions['db']
    db.create_tables()
    yield db
    db.session.close()
    db.connection.close()


@pytest.fixture
def application(create_test_db, database_url):
    app = get_app(database_url=database_url)
    return app


@pytest.fixture
def client(application):
    return TestApp(application)


@pytest.fixture
def recipe():
    recipe = Recipe(
        name='Simple Scrambled Eggs',
        prep_time=timedelta(minutes=5),
        difficulty=1,
        vegetarian=True,
    )
    return recipe


@pytest.fixture
def saved_recipe(database, recipe):
    database.session.add(recipe)
    database.session.commit()
    return recipe


@pytest.fixture
def recipe_data():
    return {
        'name': 'Simple Scrambled Eggs',
        'prep_time': 5,  # minutes
        'difficulty': 1,
        'vegetarian': True,
    }
