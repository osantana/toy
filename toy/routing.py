import re

from .exceptions import InvalidRouteHandlerException
from . import handlers


class Route:
    def __init__(self, path, handler):
        if not path:
            raise ValueError('Invalid path')
        self.path = path

        if not callable(handler):
            raise InvalidRouteHandlerException('Handlers must be callable objects')
        self.handler = handler

        self.pattern = re.compile(path)
        self.path_arguments = {}

    def match(self, path):
        match = self.pattern.search(path)
        if not match:
            return

        self.path_arguments.update(match.groupdict())

        return self.path_arguments

    def __repr__(self):
        return f'<Route {self.path} {self.handler.__class__.__name__}>'

    def __eq__(self, other):
        return self.pattern == other.pattern and self.handler == other.handler


class Routes:
    def __init__(
            self,
            routes=None,
            not_found=handlers.not_found_handler,
            internal_error=handlers.internal_error_handler,
            unauthorized=handlers.unauthorized_handler,
            unsupported_media_type=handlers.unsupported_media_type_handler,
    ):
        if routes is None:
            routes = []

        self._routes = routes
        self.not_found = not_found
        self.internal_error = internal_error
        self.unauthorized = unauthorized
        self.unsupported_media_type = unsupported_media_type

    def __len__(self):
        return len(self._routes)

    def __getitem__(self, item):
        return self._routes[item]

    def add(self, route: Route):
        if [r for r in self._routes if r == route]:
            raise ValueError('Duplicated route/handler')

        self._routes.append(route)

    def add_route(self, path, handler):
        self.add(Route(path, handler))

    def match(self, path):
        return [route for route in self._routes if route.match(path) is not None]
