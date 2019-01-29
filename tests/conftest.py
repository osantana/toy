import pytest

from toy.application import Application


@pytest.fixture
def database_url():
    return 'sqlite:///:memory:'


@pytest.fixture
def application(database_url):
    return Application(database_url=database_url)
