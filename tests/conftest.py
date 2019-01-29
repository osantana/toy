import pytest


@pytest.fixture
def connect_url():
    return 'sqlite:///:memory:'
