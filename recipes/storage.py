from recipes.models import Rating, Recipe, User


class Storage:
    def __init__(self, db_config):
        self.db_config = db_config

    def initialize_database(self):
        pass
    
    def get_recipes(self, offset=0, limit=50, search=None):
        pass

    def get_recipe(self, id_: str) -> Recipe:
        pass

    def save_recipe(self, recipe: Recipe):
        pass

    def add_rating(self, recipe: Recipe, rating: Rating):
        pass

    def get_user(self, username) -> User:
        pass

    def add_user(self, username, password):
        pass
