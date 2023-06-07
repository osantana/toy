from prettyconf import config

from toy.application import Application

from . import handlers
from .database import get_db


class RecipesApp(Application):
    def initialize(self):
        self.config['debug'] = config('DEBUG', default=False, cast=config.boolean)
        self.config.setdefault('database_url', config('DATABASE_URL'))

        recipe_handler = handlers.Recipe(application=self)
        self.add_route(r'^/recipes$', handlers.Recipes(application=self))  # GET only
        self.add_route(r'^/recipes$', recipe_handler)  # POST only
        self.add_route(r'^/recipes/(?P<id>[0-9a-f-]+)$', recipe_handler)
        self.add_route(r'^/recipes/(?P<id>[0-9a-f-]+)/rating$', handlers.Rating(application=self))


def get_app(**kwargs):
    app = RecipesApp(**kwargs)
    get_db(app)
    return app