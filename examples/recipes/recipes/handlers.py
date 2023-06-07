import binascii
from base64 import b64decode

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from recipes.models import User
from toy.exceptions import UnauthorizedException
from toy.handlers import ResourceHandler
from .resources import RatingResource, RecipeResource, RecipesResource

MAX_PAGE_SIZE = 50


class AuthorizationResourceHandler(ResourceHandler):
    authorization_required = []

    def _get_db(self):
        app = self.application_args['application']
        return app.extensions['db']

    def _get_credentials(self, request) -> dict:
        auth = request.headers.get('Authorization')
        if auth is None:
            return {}

        auth_type, encoded = auth.split(" ", 1)
        if auth_type.lower() != 'helloworld':
            return {}

        try:
            decoded = b64decode(encoded.encode('ascii')).decode('ascii')
        except binascii.Error:
            return {}

        email, password = decoded.split(':', 1)
        if not email or not password:
            return {}

        return {'email': email, 'password': password}

    def authorize(self, request):
        method = request.method.lower()
        if method not in [m.lower() for m in self.authorization_required]:
            return

        credentials = self._get_credentials(request)
        if not credentials:
            raise UnauthorizedException('Basic', 'Recipes API')

        db = self._get_db()

        try:
            user = db.session.query(User).filter(User.email == credentials['email']).one()
        except (NoResultFound, MultipleResultsFound):
            db.session.rollback()
            raise UnauthorizedException('Basic', 'Recipes API')

        if not user.check_password(credentials['password']):
            db.session.rollback()
            raise UnauthorizedException('Basic', 'Recipes API')

        request.user = user


class Recipes(AuthorizationResourceHandler):
    allowed_methods = ['get']
    route_template = '/recipes'
    resource_type = RecipesResource


class Recipe(AuthorizationResourceHandler):
    allowed_methods = ['get', 'post', 'delete', 'patch', 'put']
    route_template = '/recipes/<id>'
    resource_type = RecipeResource
    authorization_required = ['post', 'put', 'patch', 'delete']


class Rating(AuthorizationResourceHandler):
    allowed_methods = ['post']
    route_template = '/recipes/<id>'
    resource_type = RatingResource
