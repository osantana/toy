import re

from .exceptions import InvalidRouteHandler
from .handlers import internal_error_handler, not_found_handler


class Route:
    def __init__(self, path, handler):
        if not path:
            raise ValueError('Invalid path')
        self.path = path

        if not callable(handler):
            raise InvalidRouteHandler('Handlers must be callable objects')
        self.handler = handler

        self.pattern = re.compile(path)
        self.args = {}

    def match(self, path):
        match = self.pattern.search(path)
        if not match:
            return

        self.args.update(match.groupdict())

        return self.args

    def __repr__(self):
        return f'<Route {self.path} {self.handler.__class__.__name__}>'


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
        if route.path in self._routes:
            self._routes[route.path].append(route)
        else:
            self._routes[route.path] = [route]

    def add_route(self, path, handler):
        self.add(Route(path, handler))

    def match(self, path):
        matches = []
        for routes in self._routes.values():
            matches.extend(route for route in routes if route.match(path) is not None)
        return matches
