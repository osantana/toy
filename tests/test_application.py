from recipes.application import RecipesApp


def test_basic_recipes_app():
    application = RecipesApp()

    assert 'database_url' in application.config
    assert 'debug' in application.config
    assert len(application.routes) == 4
