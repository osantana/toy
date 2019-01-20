from .http import Request, Response, WSGIResponse
from .routing import Routes


class Application:
    def __init__(self):
        self.routes = Routes()

    def add_route(self, path, handler):
        self.routes.add_route(path, handler)

    def call_handler(self, request: Request) -> Response:
        path = request.path
        route = self.routes.match(path)
        kwargs = route.match(request.path)
        return route.handler(request, **kwargs)

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.call_handler(request)
        wsgi_response = WSGIResponse(response)

        start_response(wsgi_response.status, wsgi_response.headers)
        return wsgi_response.body
