from uuid import UUID


def test_create_recipe(client, database):
    recipe_data = {
        'name': 'Simple Scrambled Eggs',
        'prep_time': 5,  # minutes
        'difficulty': 1,
        'vegetarian': True,
    }
    response = client.post_json('/recipes', recipe_data)
    json = response.json
    recipe_id = json['id']

    assert response.status == '201 Created'
    assert response.headers['Location'] == f'/recipes/{recipe_id}'

    assert UUID(recipe_id)
    assert json['name'] == 'Simple Scrambled Eggs'
    assert json['prep_time'] == 5
    assert json['difficulty'] == 1
    assert json['vegetarian'] is True
    assert json['ratings'] == []
