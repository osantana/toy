from base64 import b64encode
from datetime import timedelta

import pytest
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database, drop_database
from webtest import TestApp

from recipes.application import get_app
from recipes.models import Rating, Recipe, User


@pytest.fixture
def database_url():
    return 'postgresql://recipesapi:recipesapi@localhost/test_recipesapi'


@pytest.fixture
def create_test_db(database_url):
    try:
        drop_database(database_url)
    except ProgrammingError:
        pass

    create_database(database_url)
    yield

    # FIXME: https://github.com/Overseas-Student-Living/sqlalchemy-diff/issues/10
    while True:
        try:
            drop_database(database_url)
        except ProgrammingError:
            continue
        break


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


@pytest.fixture
def recipes(recipe_data, database):
    objs = []
    for i in range(35):
        recipe = Recipe(
            name=f'{recipe_data["name"]} #{i}',
            prep_time=timedelta(minutes=recipe_data['prep_time']),
            difficulty=recipe_data['difficulty'],
            vegetarian=recipe_data['vegetarian'],
        )
        database.session.add(recipe)
        objs.append(recipe)
    database.session.commit()
    database.session.flush()
    return objs


@pytest.fixture
def user(database):
    user = User(
        email='test@example.com',
    )
    user.set_password('sekret')
    database.session.add(user)
    database.session.commit()
    return user


@pytest.fixture
def user_credentials(user):
    credentials = b64encode(f'{user.email}:sekret'.encode('ascii')).decode('ascii')
    headers = {
        'Authorization': f'Basic {credentials}',
    }
    return headers


@pytest.fixture
def unknown_user(user):
    credentials = b64encode(f'{user.email}:wrong-password'.encode('ascii')).decode('ascii')
    headers = {
        'Authorization': f'Basic {credentials}',
    }
    return headers
