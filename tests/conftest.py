from datetime import timedelta

import pytest
from webtest import TestApp

from recipes.application import get_app
from recipes.models import Recipe


@pytest.fixture
def database_url():
    return 'sqlite:///:memory:'


@pytest.fixture
def application(database_url):
    app = get_app(database_url=database_url)
    return app


@pytest.fixture
def client(application):
    return TestApp(application)


@pytest.fixture
def recipe():
    return Recipe(
        name='Scrambled Eggs',
        prep_time=timedelta(minutes=10),
        difficulty=1,
        vegetarian=True,
    )
