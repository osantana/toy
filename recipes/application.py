from prettyconf import config

from .database import get_db
from toy.application import Application
from . import handlers


class Recipes(Application):
    def initialize(self):
        self.config['debug'] = config('DEBUG', default=False, cast=config.boolean)
        self.config['database_url'] = config('DATABASE_URL')

        recipe_handler = handlers.Recipe(application=self)
        self.add_route(r'/recipes', handlers.Recipes(application=self))  # GET only
        self.add_route(r'/recipes', recipe_handler)  # POST
        self.add_route(r'/recipes/(?P<id>\d+)', recipe_handler)
        self.add_route(r'/recipes/(?P<id>\d+)/rating', handlers.Rating(application=self))


def get_app():
    app = Recipes()
    get_db(app)
    return app
