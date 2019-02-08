def test_create_recipe(client, application):
    recipe_data = {
        'name': 'Simple Scrambled Eggs',
        'prep_time': 5,  # minutes
        'difficulty': 1,
        'vegetarian': True,
    }
    response = client.post_json('/recipes', recipe_data)

    assert response.status == '201 Created'
