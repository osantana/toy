from toy.application import Application

from . import handlers


def get_app():
    app = Application()
    app.debug = True
    app.add_route(r'/recipes', handlers.Recipes())
    app.add_route(r'/recipes/(?P<id>\d+)', handlers.Recipe())
    app.add_route(r'/recipes/(?P<id>\d+)/rating', handlers.Recipe())
    return app
