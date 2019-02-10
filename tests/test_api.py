from datetime import timedelta
from uuid import UUID

from recipes.models import Rating, Recipe


def test_create_recipe(client, database):
    recipe_data = {
        'name': 'Simple Scrambled Eggs',
        'prep_time': 5,  # minutes
        'difficulty': 1,
        'vegetarian': True,
        'ratings': [
            {'value': 5}
        ]
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
    assert json['ratings'][0]['value'] == 5
    assert json['ratings'][0]['id'] is not None


def test_create_recipe_in_database(client, recipe_data, database):
    client.post_json('/recipes', recipe_data)

    recipes = database.session.query(Recipe).all()
    assert len(recipes) == 1
    assert recipes[0].name == 'Simple Scrambled Eggs'
    assert recipes[0].prep_time == timedelta(minutes=5)
    assert recipes[0].difficulty == 1
    assert recipes[0].vegetarian is True
    assert len(recipes[0].ratings) == 1
    assert recipes[0].ratings[0].value == 5


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


def test_get_recipe(client, saved_recipe, database):
    response = client.get(
        f'/recipes/{saved_recipe.id}',
        headers={'Accept': 'application/json'},
    )
    assert response.status == '200 OK'

    json = response.json
    assert json['id'] == str(saved_recipe.id)
    assert json['name'] == 'Simple Scrambled Eggs'
    assert json['prep_time'] == 5
    assert json['difficulty'] == 1
    assert json['vegetarian'] is True
    assert len(json['ratings']) == 1


def test_fail_get_unknown_recipe(client, database):
    response = client.get(
        f'/recipes/deadbeef-c1a1-424d-b45f-52d5641c623c',  # unknown
        headers={'Accept': 'application/json'},
        status=404,
    )
    assert response.status == '404 Not Found'

    json = response.json
    assert json['errors'][0] == 'Not Found'


def test_delete_recipe(client, saved_recipe, database):
    response = client.delete(
        f'/recipes/{saved_recipe.id}',
        headers={'Accept': 'application/json'},
    )
    assert response.status == '204 No Content'

    recipes = database.session.query(Recipe).all()
    assert len(recipes) == 0


def test_fail_delete_unknown_recipe(client, database):
    response = client.delete(
        f'/recipes/deadbeef-c1a1-424d-b45f-52d5641c623c',  # unknown
        headers={'Accept': 'application/json'},
        status=404,
    )
    assert response.status == '404 Not Found'

    json = response.json
    assert json['errors'][0] == 'Not Found'


def test_replace_recipe(client, saved_recipe, database):
    new_recipe_data = {
        'name': 'Super Scrambled Eggs',
        'prep_time': 10,  # minutes
        'difficulty': 2,
        'vegetarian': True,
        'ratings': [
            {'value': 2},
            {'value': 1},
        ]
    }
    response = client.put_json(f'/recipes/{saved_recipe.id}', new_recipe_data)
    assert response.status == '200 OK'

    json = response.json

    assert json['id'] == str(saved_recipe.id)
    assert json['name'] == 'Super Scrambled Eggs'
    assert json['prep_time'] == 10
    assert json['difficulty'] == 2
    assert json['vegetarian'] is True
    assert len(json['ratings']) == 2
    assert json['ratings'][0]['value'] == 2
    assert json['ratings'][1]['value'] == 1


def test_replace_recipe_with_ratings_in_database(client, saved_rated_recipe, database):
    new_recipe_data = {
        'name': 'Super Scrambled Eggs',
        'prep_time': 10,  # minutes
        'difficulty': 2,
        'vegetarian': True,
        'ratings': [
            {'value': 5},
            {'value': 4},
        ]
    }
    client.put_json(f'/recipes/{saved_rated_recipe.id}', new_recipe_data)

    recipe = database.session.query(Recipe).first()
    assert recipe.name == new_recipe_data['name']
    assert recipe.prep_time == timedelta(minutes=new_recipe_data['prep_time'])
    assert recipe.difficulty == new_recipe_data['difficulty']
    assert recipe.vegetarian == new_recipe_data['vegetarian']
    assert len(recipe.ratings) == 2
    assert recipe.ratings[0].value == 5
    assert recipe.ratings[1].value == 4


def test_fail_replace_recipe_with_incomplete_payload(client, saved_rated_recipe, database):
    new_recipe_data = {
        'name': 'Super Scrambled Eggs',
        'prep_time': 10,  # minutes
        'difficulty': 2,
        'vegetarian': True,
    }
    response = client.put_json(f'/recipes/{saved_rated_recipe.id}', new_recipe_data, status=400)
    assert response.status == '400 Bad Request'

    json = response.json
    assert json['errors'][0].startswith("Invalid resource fields ")

    # check old values is preserved
    recipe = database.session.query(Recipe).first()
    assert recipe.name == saved_rated_recipe.name
    assert recipe.prep_time == saved_rated_recipe.prep_time
    assert recipe.difficulty == saved_rated_recipe.difficulty
    assert recipe.vegetarian == saved_rated_recipe.vegetarian
    assert len(recipe.ratings) == 2
    assert recipe.ratings[0].value == 5
    assert recipe.ratings[1].value == 1


def test_change_recipe(client, saved_recipe, database):
    new_recipe_data = {
        'name': 'Super Scrambled Eggs',
        'ratings': [
            {'value': 2},
            {'value': 1},
        ]
    }
    response = client.patch_json(f'/recipes/{saved_recipe.id}', new_recipe_data)
    assert response.status == '200 OK'

    json = response.json

    assert json['id'] == str(saved_recipe.id)
    assert json['name'] == 'Super Scrambled Eggs'
    assert json['prep_time'] == 5
    assert json['difficulty'] == 1
    assert json['vegetarian'] is True
    assert len(json['ratings']) == 2
    assert json['ratings'][0]['value'] == 2
    assert json['ratings'][1]['value'] == 1


def test_change_recipe_with_ratings_in_database(client, saved_recipe, database):
    new_recipe_data = {
        'name': 'Super Scrambled Eggs',
        'ratings': [
            {'value': 2},
            {'value': 1},
        ]
    }
    client.patch_json(f'/recipes/{saved_recipe.id}', new_recipe_data)

    recipe = database.session.query(Recipe).first()
    assert recipe.name == new_recipe_data['name']
    assert recipe.prep_time == saved_recipe.prep_time
    assert recipe.difficulty == saved_recipe.difficulty
    assert recipe.vegetarian == saved_recipe.vegetarian
    assert len(recipe.ratings) == 2
    assert recipe.ratings[0].value == 2
    assert recipe.ratings[1].value == 1


def test_create_rating(client, saved_recipe, database):
    rating_data = {'value': 3}
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
    assert len(json['ratings']) == 2
    assert json['ratings'][0]['value'] == 5
    assert json['ratings'][1]['value'] == 3


def test_create_rating_in_database(client, saved_recipe, database):
    rating_data = {'value': 3}
    client.post_json(f'/recipes/{saved_recipe.id}/rating', rating_data)

    ratings = database.session.query(Rating).filter(Rating.recipe == saved_recipe).all()

    assert len(ratings) == 2
    assert ratings[0].value == 5
    assert ratings[1].value == 3


def test_fail_create_rating_missing_required_field(client, saved_recipe, database):
    rating_data = {}  # missing value
    response = client.post_json(f'/recipes/{saved_recipe.id}/rating', rating_data, status=400)
    assert response.status == '400 Bad Request'

    errors = response.json['errors']

    assert errors[0]['field'] == 'value'
    assert errors[0]['message'] == 'Required field'
    assert errors[1]['field'] == 'value'
    assert errors[1]['message'] == 'Invalid value type for this field'
