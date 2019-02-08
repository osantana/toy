from datetime import timedelta

from recipes.models import Recipe
from toy import fields
from toy.resources import Resource


class RatingResource(Resource):
    fields = [
        fields.UUIDField(name='id', required=True, lazy=True),
        fields.IntegerField(name='value', min_value=1, max_value=5),
    ]


class RecipeResource(Resource):
    fields = [
        fields.UUIDField(name='id', required=True, lazy=True),
        fields.CharField(name='name', max_length=255, required=True),
        fields.IntegerField(name='prep_time', min_value=0, required=True),
        fields.IntegerField(name='difficulty', min_value=1, max_value=3, required=True),
        fields.BooleanField(name='vegetarian', required=True),
        fields.ResourceListField(name='ratings', resource_type=RatingResource),
    ]

    def _get_db(self):
        app = self.application_args['application']
        return app.extensions['db']

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


class RecipesResource(Resource):
    pass  # TODO
