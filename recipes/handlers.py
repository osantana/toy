from toy.handlers import ResourceHandler
from .resources import RatingResource, RecipeResource, RecipesResource

MAX_PAGE_SIZE = 50


class Recipes(ResourceHandler):
    route_template = '/recipes'
    resource_type = RecipesResource


class Recipe(ResourceHandler):
    allowed_methods = ['post']
    route_template = '/recipes/<id>'
    resource_type = RecipeResource


class Rating(ResourceHandler):
    allowed_methods = ['post']
    route_template = '/recipes/<id>'
    resource_type = RatingResource
