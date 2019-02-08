from datetime import timedelta
from uuid import UUID

from recipes.models import Rating, Recipe
from toy import fields
from toy.resources import Resource


class BaseResource(Resource):
    def _get_db(self):
        app = self.application_args['application']
        return app.extensions['db']


class RatingResource(BaseResource):
    fields = [
        fields.UUIDField(name='id', required=True, lazy=True),
        fields.IntegerField(name='value', min_value=1, max_value=5),
    ]

    def do_create(self):
        db = self._get_db()

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
        db = self._get_db()

        recipe = Recipe(
            name=self['name'],
            prep_time=timedelta(minutes=self['prep_time']),
            difficulty=self['difficulty'],
            vegetarian=self['vegetarian'],
        )

        db.session.add(recipe)
        db.session.commit()

        self['id'] = recipe.id


class RecipesResource(BaseResource):
    pass  # TODO
