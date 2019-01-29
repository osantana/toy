from prettyconf import config

from .database import Database
from toy.application import Application
from . import handlers


class Recipes(Application):
    def initialize(self):
        self.debug = config('DEBUG', default=False, cast=config.boolean)

        recipe_handler = handlers.Recipe(application=self)
        self.add_route(r'/recipes', handlers.Recipes(application=self))  # GET only
        self.add_route(r'/recipes', recipe_handler)  # POST
        self.add_route(r'/recipes/(?P<id>\d+)', recipe_handler)
        self.add_route(r'/recipes/(?P<id>\d+)/rating', handlers.Rating(application=self))

        database_url = config('DATABASE_URL')
        db = Database.get(database_url, echo=self.debug)
        self.add_extension('db', db)


def get_app():
    return Recipes()
