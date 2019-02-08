from datetime import timedelta
from uuid import UUID

from recipes.models import Recipe


def test_create_recipe(client, database):
    recipe_data = {
        'name': 'Simple Scrambled Eggs',
        'prep_time': 5,  # minutes
        'difficulty': 1,
        'vegetarian': True,
    }
    response = client.post_json('/recipes', recipe_data)
    assert response.status == '201 Created'

    json = response.json
    recipe_id = json['id']

    assert response.headers['Location'] == f'/recipes/{recipe_id}'
    assert UUID(recipe_id)
    assert json['name'] == 'Simple Scrambled Eggs'
    assert json['prep_time'] == 5
    assert json['difficulty'] == 1
    assert json['vegetarian'] is True
    assert json['ratings'] == []


def test_create_recipe_in_database(client, recipe_data, database):
    client.post_json('/recipes', recipe_data)

    users = database.session.query(Recipe).all()
    assert len(users) == 1
    assert users[0].name == 'Simple Scrambled Eggs'
    assert users[0].prep_time == timedelta(minutes=5)
    assert users[0].difficulty == 1
    assert users[0].vegetarian is True
    assert users[0].ratings == []
