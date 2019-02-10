from staty import HTTPError, MethodNotAllowed, MethodNotAllowedException, NotFoundException

from toy.exceptions import UnauthorizedException
from .http import Request, Response, WSGIResponse
from .routing import Routes


class Application:
    def __init__(self, **kwargs):
        self.routes = Routes()
        self.extensions = {}
        self.config = {
            'debug': False,
        }

        self.config.update(kwargs)

        self.initialize()

    def initialize(self):
        pass

    @property
    def debug(self):
        return self.config.get('debug', False)

    @debug.setter
    def debug(self, value):
        self.config['debug'] = value

    def add_extension(self, key, value):
        if key in self.extensions:
            raise KeyError(f'Key {key} already exists')
        self.extensions[key] = value
        value.application = self

    def get_extension(self, key, default=None):
        return self.extensions.get(key, default)

    def add_route(self, path, handler):
        self.routes.add_route(path, handler)

    def call_handler(self, request: Request) -> Response:
        path = request.path
        routes = self.routes.match(path)

        if not routes:
            return self.routes.not_found(request)

        for route in routes:
            request.path_arguments.update(route.path_arguments)

            # noinspection PyBroadException
            try:
                response = route.handler(request)
            except MethodNotAllowedException:
                continue

            except NotFoundException:
                return self.routes.not_found(request)

            except UnauthorizedException as ex:
                return self.routes.unauthorized(request, ex)

            except HTTPError as ex:
                response = Response(str(ex), status=ex.status)

            # We need to intercept all exceptions to return appropriate 500 response
            except Exception:
                if self.debug:
                    raise
                return self.routes.internal_error(request)

            return response

        return Response(f'Method {request.method} not allowed', status=MethodNotAllowed())

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.call_handler(request)
        wsgi_response = WSGIResponse(response)

        start_response(wsgi_response.status, wsgi_response.headers)
        return wsgi_response.body
