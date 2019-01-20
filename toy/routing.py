import re

from .handlers import not_found_handler, internal_error_handler
from .exceptions import InvalidRouteHandler


class Route:
    def __init__(self, path, handler):
        if not path:
            raise ValueError('Invalid path')
        self.path = path

        if not callable(handler):
            raise InvalidRouteHandler('Handlers must be callable objects')
        self.handler = handler

        self.pattern = re.compile(path)

    def match(self, path):
        match = self.pattern.search(path)
        if not match:
            return
        return match.groupdict()


class Routes:
    def __init__(
            self,
            routes=None,
            not_found=not_found_handler,
            internal_error=internal_error_handler,
    ):
        self._routes = {}

        if routes is None:
            routes = []

        for route in routes:
            self.add(route)

        self.not_found = not_found
        self.internal_error = internal_error

    def __len__(self):
        return len(self._routes)

    def __getitem__(self, path):
        return self._routes[path]

    def add(self, route: Route):
        self._routes[route.path] = route

    def add_route(self, path, handler):
        self.add(Route(path, handler))

    def match(self, path):
        for route in self._routes.values():
            if route.match(path) is not None:
                return route
