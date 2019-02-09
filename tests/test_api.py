from datetime import timedelta
from uuid import UUID

from recipes.models import Rating, Recipe


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

    recipes = database.session.query(Recipe).all()
    assert len(recipes) == 1
    assert recipes[0].name == 'Simple Scrambled Eggs'
    assert recipes[0].prep_time == timedelta(minutes=5)
    assert recipes[0].difficulty == 1
    assert recipes[0].vegetarian is True
    assert recipes[0].ratings == []


def test_fail_create_recipe_missing_required_field(client, database):
    recipe_data = {
        # 'name': 'Simple Scrambled Eggs',  # missing field
        'prep_time': 5,  # minutes
        'difficulty': 1,
        'vegetarian': True,
    }
    response = client.post_json('/recipes', recipe_data, status=400)
    assert response.status == '400 Bad Request'

    errors = response.json['errors']
    assert errors[0]['field'] == 'name'
    assert errors[0]['message'] == 'Required field'


def test_create_rating(client, saved_recipe, database):
    rating_data = {'value': 5}
    response = client.post_json(f'/recipes/{saved_recipe.id}/rating', rating_data)
    assert response.status == '201 Created'

    json = response.json
    recipe_id = json['id']

    assert response.headers['Location'] == f'/recipes/{recipe_id}'
    assert UUID(recipe_id)
    assert json['name'] == 'Simple Scrambled Eggs'
    assert json['prep_time'] == 5
    assert json['difficulty'] == 1
    assert json['vegetarian'] is True
    assert len(json['ratings']) == 1


def test_create_rating_in_database(client, saved_recipe, database):
    rating_data = {'value': 5}
    client.post_json(f'/recipes/{saved_recipe.id}/rating', rating_data)

    ratings = database.session.query(Rating).filter(Rating.recipe == saved_recipe).all()

    assert len(ratings) == 1
    assert ratings[0].value == 5


def test_fail_create_rating_missing_required_field(client, saved_recipe, database):
    rating_data = {}  # missing value
    response = client.post_json(f'/recipes/{saved_recipe.id}/rating', rating_data, status=400)
    assert response.status == '400 Bad Request'

    errors = response.json['errors']

    assert errors[0]['field'] == 'value'
    assert errors[0]['message'] == 'Required field'
    assert errors[1]['field'] == 'value'
    assert errors[1]['message'] == 'Invalid value type for this field'
