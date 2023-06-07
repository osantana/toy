from datetime import timedelta
from uuid import UUID

from sqlalchemy import func
from sqlalchemy_searchable import search

from recipes.models import Rating, Recipe
from toy import fields
from toy.exceptions import ResourceNotFoundException, ValidationError, ValidationException
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
            raise ResourceNotFoundException('Parent recipe not found')

        recipe = db.session.query(Recipe).get(recipe_id)
        if not recipe:
            db.session.rollback()
            raise ResourceNotFoundException('Parent recipe not found')

        rating = Rating(value=self['value'])
        recipe.ratings.append(rating)
        db.session.commit()

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

    @classmethod
    def _get_object_or_not_found(cls, db, request):
        try:
            recipe_id = request.path_arguments['id']
        except KeyError:
            raise ResourceNotFoundException('Unknown path id')
        recipe = db.session.query(Recipe).get(recipe_id)
        if not recipe:
            db.session.rollback()
            raise ResourceNotFoundException(f'Recipe {recipe_id} not found')
        return recipe

    def _load_object_or_not_found(self, db):
        recipe = self._get_object_or_not_found(db, self.request)
        self['id'] = recipe.id
        return recipe

    def load_from_model(self, recipe):
        self['id'] = recipe.id
        self['name'] = recipe.name
        self['prep_time'] = recipe.prep_time.total_seconds() // 60
        self['difficulty'] = recipe.difficulty
        self['vegetarian'] = recipe.vegetarian

        for rating in recipe.ratings:
            self['ratings'].append(
                RatingResource(
                    request=self.request,
                    application_args=self.application_args,
                    id=rating.id,
                    value=rating.value,
                )
            )

    def save_to_model(self, recipe, db=None):
        recipe.name = self['name']
        recipe.prep_time = timedelta(minutes=self['prep_time'])
        recipe.difficulty = self['difficulty']
        recipe.vegetarian = self['vegetarian']

        if not db:
            return

        db.session.query(Rating).filter(recipe == recipe).delete()
        for rating in self['ratings']:
            rating.create(parent_resource=self)

    @classmethod
    def do_get(cls, request=None, application_args=None):
        db = cls._get_db(application_args)

        recipe = cls._get_object_or_not_found(db, request=request)

        resource = cls(
            request=request,
            application_args=application_args,
        )
        resource.load_from_model(recipe)
        return resource

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

        db.session.commit()

    def do_remove(self):
        db = self._get_db(self.application_args)
        recipe = self._load_object_or_not_found(db)
        db.session.delete(recipe)
        db.session.commit()

    def do_replace(self):
        db = self._get_db(self.application_args)
        recipe = self._load_object_or_not_found(db)

        self.save_to_model(recipe, db)
        db.session.commit()

    def do_change(self, **kwargs):
        db = self._get_db(self.application_args)
        recipe = self._load_object_or_not_found(db)

        self.load_from_model(recipe)

        kwargs.pop('id', None)  # FIXME: cannot update id. raise error?
        self.update(kwargs)

        self.save_to_model(recipe, db if 'ratings' in kwargs else None)
        db.session.commit()


class RecipesResource(BaseResource):
    fields = [
        fields.IntegerField(name='offset'),
        fields.IntegerField(name='limit'),
        fields.IntegerField(name='total'),
        fields.IntegerField(name='count'),
        fields.ResourceListField(name='results', resource_type=RecipeResource),
        fields.CharField(name='search', max_length=255),
    ]

    default_limit = 20
    max_limit = 30
    default_offset = 0

    @classmethod
    def do_get(cls, request=None, application_args=None):

        errors = {}

        limit = request.query_string.get('limit')
        try:
            limit = [cls.default_limit] if limit is None else limit
            limit = min(cls.max_limit, int(limit[-1]))
        except ValueError:
            errors['limit'] = [ValidationError('Invalid value', 'limit', limit)]

        offset = request.query_string.get('offset')
        try:
            offset = [cls.default_offset] if offset is None else offset
            offset = int(offset[-1])
        except ValueError:
            errors['offset'] = [ValidationError('Invalid value', 'offset', offset)]

        if errors:
            raise ValidationException('Invalid query', errors)

        search_terms = request.query_string.get('search')
        search_terms = [None] if search_terms is None else search_terms
        search_terms = search_terms[-1]

        resource = cls(
            request=request,
            application_args=application_args,
            offset=offset,
            limit=limit,
            search=search_terms,
        )

        db = cls._get_db(application_args)
        resource['total'] = db.session.query(func.count(Recipe.id)).scalar()

        query = db.session.query(Recipe)
        if resource['search']:
            query = search(query, resource['search'], sort=True)

        query = query.offset(resource['offset'])
        query = query.limit(resource['limit'])

        recipes = []
        for recipe in query.all():
            recipe_resource = RecipeResource(
                request=request,
                application_args=application_args,
            )
            recipe_resource.load_from_model(recipe)
            recipes.append(recipe_resource)
        resource['results'] = recipes
        resource['count'] = len(recipes)

        return resource
