import re
from unittest.mock import Mock

import pytest
from webtest import TestApp

from recipes.framework.application import Application
from recipes.framework.exceptions import InvalidRouteHandler
from recipes.framework.routing import Route, Routes


def test_basic_application():
    app = Application()

    assert callable(app), "It's not a WSGI middleware"
    assert len(app.routes) == 0


def test_basic_request_to_app(application):
    handler = Mock()
    application.add_route(r'^/test', handler)

    app = TestApp(application)

    response = app.get("/test")
    assert response


def test_basic_route(handler):
    route = Route(r'^/$', handler)

    assert route.path == r'^/$'
    assert route.pattern == re.compile(r'^/$')
    assert route.handler == handler
    assert route.match('/') == {}
    assert route.match('/dont-match') is None


def test_route_with_args(handler):
    route = Route(r'^/(?P<arg>.*)$', handler)

    assert route.match('/') == {'arg': ''}
    assert route.match('/value') == {'arg': 'value'}


def test_error_route_with_not_callable_handler():
    with pytest.raises(InvalidRouteHandler):
        Route(r'^$', "not-callable")


def test_error_route_with_no_path(handler):
    with pytest.raises(ValueError):
        Route('', handler)


def test_basic_routes(handler):
    routes = Routes([
        Route(r'^/$', handler)
    ])

    assert len(routes) == 1
    assert routes[r'^/$'].path == '^/$'


def test_add_routes(handler):
    routes = Routes([
        Route('^/1$', handler)
    ])
    routes.add(Route(r'^/2$', handler))
    routes.add_route(r'^/3$', handler)

    assert len(routes) == 3
    assert routes['^/1$'].path == '^/1$'
    assert routes['^/2$'].path == '^/2$'
    assert routes['^/3$'].path == '^/3$'


def test_match_route_in_routes(handler):
    routes = Routes()
    routes.add_route(r'^/$', handler)
    routes.add_route(r'^/(?P<arg>.*)$', handler)

    assert routes.match("/").path == r'^/$'
    assert routes.match("/resources").path == r'^/(?P<arg>.*)$'
