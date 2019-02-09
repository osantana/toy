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

    def do_create(self, parent_resource=None):
        db = self._get_db(self.application_args)

        if parent_resource:
            recipe_id = parent_resource['id']
        else:
            recipe_id = UUID(self.request.path_arguments.get('id'))

        if not recipe_id:
            raise ResourceNotFound('Parent recipe not found')

        recipe = db.session.query(Recipe).get(recipe_id)
        if not recipe:
            raise ResourceNotFound('Parent recipe not found')

        rating = Rating(value=self['value'])
        recipe.ratings.append(rating)
        db.session.commit()
        db.session.flush()

        self['id'] = rating.id

        if not parent_resource:
            parent_resource = RecipeResource(
                id=recipe.id,
                name=recipe.name,
                prep_time=recipe.prep_time.total_seconds() / 60,
                difficulty=recipe.difficulty,
                vegetarian=recipe.vegetarian,
            )
            for rating in recipe.ratings:
                rating_resource = RatingResource(
                    id=rating.id,
                    value=rating.value,
                )
                parent_resource['ratings'].append(rating_resource)

        return parent_resource


class RecipeResource(BaseResource):
    fields = [
        fields.UUIDField(name='id', required=True, lazy=True),
        fields.CharField(name='name', max_length=255, required=True),
        fields.IntegerField(name='prep_time', min_value=0, required=True),
        fields.IntegerField(name='difficulty', min_value=1, max_value=3, required=True),
        fields.BooleanField(name='vegetarian', required=True),
        fields.ResourceListField(name='ratings', resource_type=RatingResource),
    ]

    def do_create(self, parent_resource=None):
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
        for rating in self['ratings']:
            rating.create(parent_resource=self)

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
        )

        for rating in recipe.ratings:
            resource['ratings'].append(
                RatingResource(
                    id=rating.id,
                    value=rating.value,
                )
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

    def do_replace(self):
        db = self._get_db(self.application_args)

        try:
            recipe_id = self.request.path_arguments['id']
        except KeyError:
            raise ResourceNotFound('Unknown path id')

        recipe = db.session.query(Recipe).get(recipe_id)
        if not recipe:
            raise ResourceNotFound(f'Recipe {recipe_id} not found')

        self['id'] = recipe.id

        recipe.name = self['name']
        recipe.prep_time = timedelta(minutes=self['prep_time'])
        recipe.difficulty = self['difficulty']
        recipe.vegetarian = self['vegetarian']
        db.session.query(Rating).filter(recipe == recipe).delete()

        for rating in self['ratings']:
            rating.create(parent_resource=self)

        db.session.commit()
        db.session.flush()


class RecipesResource(BaseResource):
    pass  # TODO
