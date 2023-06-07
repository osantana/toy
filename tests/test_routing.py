import re

import pytest

from toy.exceptions import InvalidRouteHandlerException
from toy.routing import Route, Routes


def test_basic_route(handler):
    route = Route(r'^/$', handler)

    assert route.path == r'^/$'
    assert route.pattern == re.compile(r'^/$')
    assert route.handler == handler
    assert repr(route) == '<Route ^/$ function>'
    assert route.match('/') == {}
    assert route.path_arguments == {}
    assert route.match('/dont-match') is None


def test_route_with_args(handler):
    route = Route(r'^/(?P<arg>.*)$', handler)

    assert route.match('/') == {'arg': ''}
    assert route.match('/value') == {'arg': 'value'}


def test_error_route_with_not_callable_handler():
    with pytest.raises(InvalidRouteHandlerException):
        Route(r'^$', 'not-callable')


def test_error_route_with_no_path(handler):
    with pytest.raises(ValueError):
        Route('', handler)


def test_basic_routes(handler):
    routes = Routes([Route(r'^/$', handler)])

    assert len(routes) == 1
    assert routes[0].path == '^/$'


def test_add_routes(handler):
    routes = Routes([Route('^/1$', handler)])
    routes.add(Route(r'^/2$', handler))
    routes.add_route(r'^/3$', handler)

    assert len(routes) == 3
    assert routes[0].path == '^/1$'
    assert routes[1].path == '^/2$'
    assert routes[2].path == '^/3$'


def test_match_route_in_routes(handler):
    routes = Routes()
    routes.add_route(r'^/$', handler)
    routes.add_route(r'^/(?P<arg>.+)$', handler)

    assert routes.match('/')[0].path == r'^/$'

    match = routes.match('/resources')[0]
    assert match.path == r'^/(?P<arg>.+)$'
    assert match.path_arguments == {'arg': 'resources'}


def test_match_multople_routes_in_routes(handler):
    routes = Routes()
    routes.add_route(r'^/$', handler)
    routes.add_route(r'^/(?P<arg>.*)$', handler)

    assert routes.match('/')[0].path == r'^/$'
    assert routes.match('/')[1].path == r'^/(?P<arg>.*)$'


def test_fail_add_same_route_twice(handler):
    routes = Routes()
    routes.add_route(r'/', handler)

    with pytest.raises(ValueError):
        routes.add_route(r'/', handler)
