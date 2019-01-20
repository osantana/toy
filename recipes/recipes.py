import dj_database_url
from prettyconf import config

from toy.application import Application
from . import handlers
from .storage import Storage


class Recipes(Application):
    def initialize(self):
        self.debug = config('DEBUG', default=False, cast=config.boolean)
        self.add_route(r'/recipes', handlers.Recipes())
        self.add_route(r'/recipes/(?P<id>\d+)', handlers.Recipe())
        self.add_route(r'/recipes/(?P<id>\d+)/rating', handlers.Recipe())

        db_config = config('DATABASE_URL', cast=dj_database_url.parse)
        self.add('storage', Storage(db_config))


def get_app():
    return Recipes()
