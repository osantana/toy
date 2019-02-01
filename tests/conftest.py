from datetime import timedelta

import pytest

from recipes.models import Recipe
from toy.application import Application


@pytest.fixture
def database_url():
    return 'sqlite:///:memory:'


@pytest.fixture
def application(database_url):
    return Application(database_url=database_url)


@pytest.fixture
def recipe():
    return Recipe(
        name='Scrambled Eggs',
        prep_time=timedelta(minutes=10),
        difficulty=1,
        vegetarian=True,
    )
