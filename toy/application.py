from staty import HTTPError

from .http import Request, Response, WSGIResponse
from .routing import Routes


class Application:
    def __init__(self, debug=False):
        self.routes = Routes()
        self.debug = debug
        self.extensions = {}

        self.initialize()

    def initialize(self):
        pass

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
        route = self.routes.match(path)

        if not route:
            return self.routes.not_found(request)

        kwargs = route.match(request.path)
        request.args.update(kwargs)

        # noinspection PyBroadException
        try:
            response = route.handler(request)
        except HTTPError as ex:
            response = Response(str(ex), status=ex.status)

        # We need to intercept all exceptions to return 500 reponse
        except Exception:
            if self.debug:
                raise
            return self.routes.internal_error(request)

        return response

    def __call__(self, environ, start_response):
        request = Request(self, environ)
        response = self.call_handler(request)
        wsgi_response = WSGIResponse(response)

        start_response(wsgi_response.status, wsgi_response.headers)
        return wsgi_response.body
