from datetime import timedelta
from uuid import UUID

from recipes.models import Rating, Recipe
from toy import fields
from toy.exceptions import ResourceNotFound
from toy.resources import Resource


class BaseResource(Resource):
    @staticmethod
    def _get_db(application_args):
        app = application_args['application']
        return app.extensions['db']


class RatingResource(BaseResource):
    fields = [
        fields.UUIDField(name='id', required=True, lazy=True),
        fields.IntegerField(name='value', min_value=1, max_value=5, required=True),
    ]

    def do_create(self):
        db = self._get_db(self.application_args)

        recipe_id = self.request.path_arguments['id']
        recipe = db.session.query(Recipe).get(UUID(recipe_id))

        # except KeyError, NotFound:  # TODO: raises 404 on unknown URL

        recipe_resource = RecipeResource(
            id=recipe.id,
            name=recipe.name,
            prep_time=recipe.prep_time.total_seconds() / 60,
            difficulty=recipe.difficulty,
            vegetarian=recipe.vegetarian,
            ratings=recipe.ratings,
        )

        rating = Rating(recipe_id=recipe.id, value=self['value'])
        db.session.add(rating)
        db.session.commit()

        self['id'] = rating.id
        recipe_resource['ratings'].append(self)
        return recipe_resource


class RecipeResource(BaseResource):
    fields = [
        fields.UUIDField(name='id', required=True, lazy=True),
        fields.CharField(name='name', max_length=255, required=True),
        fields.IntegerField(name='prep_time', min_value=0, required=True),
        fields.IntegerField(name='difficulty', min_value=1, max_value=3, required=True),
        fields.BooleanField(name='vegetarian', required=True),
        fields.ResourceListField(name='ratings', resource_type=RatingResource),
    ]

    def do_create(self):
        db = self._get_db(self.application_args)

        recipe = Recipe(
            name=self['name'],
            prep_time=timedelta(minutes=self['prep_time']),
            difficulty=self['difficulty'],
            vegetarian=self['vegetarian'],
        )

        db.session.add(recipe)
        db.session.commit()

        self['id'] = recipe.id

    @classmethod
    def do_get(cls, request=None, application_args=None):
        db = cls._get_db(application_args)

        try:
            recipe_id = request.path_arguments['id']
        except KeyError:
            raise ResourceNotFound('Unknown path id')

        recipe = db.session.query(Recipe).get(recipe_id)
        if not recipe:
            raise ResourceNotFound(f'Recipe {recipe_id} not found')

        resource = cls(
            id=recipe.id,
            name=recipe.name,
            prep_time=recipe.prep_time.total_seconds() / 60,
            difficulty=recipe.difficulty,
            vegetarian=recipe.vegetarian,
            ratings=recipe.ratings,  # TODO: limit the size of this list...
        )
        return resource

    def do_remove(self):
        db = self._get_db(self.application_args)

        try:
            recipe_id = self.request.path_arguments['id']
        except KeyError:
            raise ResourceNotFound('Unknown path id')

        recipe = db.session.query(Recipe).get(recipe_id)
        if not recipe:
            raise ResourceNotFound(f'Recipe {recipe_id} not found')

        db.session.delete(recipe)
        db.session.flush()


class RecipesResource(BaseResource):
    pass  # TODO
