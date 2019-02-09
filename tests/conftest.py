from datetime import timedelta

import pytest
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database, drop_database
from webtest import TestApp

from recipes.application import get_app
from recipes.models import Rating, Recipe


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
    db.session.commit()
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
def recipe_data():
    return {
        'name': 'Simple Scrambled Eggs',
        'prep_time': 5,  # minutes
        'difficulty': 1,
        'vegetarian': True,
        'ratings': [
            {'value': 5}
        ]
    }


@pytest.fixture
def recipe(recipe_data):
    recipe = Recipe(
        name=recipe_data['name'],
        prep_time=timedelta(minutes=recipe_data['prep_time']),
        difficulty=recipe_data['difficulty'],
        vegetarian=recipe_data['vegetarian'],
    )
    for rating in recipe_data['ratings']:
        recipe.ratings.append(Rating(value=rating['value']))
    return recipe


@pytest.fixture
def saved_recipe(database, recipe):
    database.session.add(recipe)
    database.session.commit()
    database.session.flush()
    return recipe


@pytest.fixture
def saved_rated_recipe(saved_recipe, database):
    saved_recipe.ratings.append(Rating(value=1))
    database.session.commit()
    return saved_recipe
