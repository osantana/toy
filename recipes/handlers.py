from toy.handlers import ResourceHandler

MAX_PAGE_SIZE = 50


class Recipes(ResourceHandler):
    route_template = '/recipes'


class Recipe(ResourceHandler):
    route_template = '/recipes/<id>'


class Rating(ResourceHandler):
    route_template = '/recipes/<id>/rating'
