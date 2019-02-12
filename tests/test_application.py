from unittest.mock import Mock

import pytest
from webtest import TestApp

from toy.application import Application
from toy.exceptions import UnauthorizedException
from toy.http import Request
from toy.staty import BadRequestException


def test_basic_application():
    app = Application()

    assert callable(app), "It's not a WSGI middleware"
    assert len(app.routes) == 0
    assert len(app.extensions) == 0
    assert len(app.config) == 1
    assert app.debug == app.config['debug']
    assert app.debug is False


def test_basic_request_to_app(application, handler):
    application.add_route(r'^/test', handler)

    client = TestApp(application)

    response = client.get('/test')

    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'
    assert response.body == 'Hello!'.encode('utf-8')


def test_request_different_methods_to_same_route_different_handlers(application, get_handler, post_handler):
    application.add_route(r'^/test', get_handler)
    application.add_route(r'^/test', post_handler)

    client = TestApp(application)

    response = client.get('/test')
    assert response.body == 'Hello GET!'.encode('utf-8')

    response = client.post('/test')
    assert response.body == 'Hello POST!'.encode('utf-8')


def test_fail_request_methods_not_allowed_in_handlers(application, get_handler, post_handler):
    application.add_route(r'^/test', post_handler)

    client = TestApp(application)

    response = client.get('/test', status=405)
    assert response.status == '405 Method Not Allowed'


def test_add_application_extension(application):
    extension = Mock()
    application.add_extension('mock_extension', extension)

    assert extension.application == application
    assert application.get_extension('mock_extension') == extension


def test_fail_add_application_extension_twice(application):
    extension = Mock()
    application.add_extension('mock_extension', extension)

    with pytest.raises(KeyError):
        application.add_extension('mock_extension', extension)


def test_request_to_not_found_route(application, handler):
    app = TestApp(application)

    response = app.get('/not-found', status=404)

    assert response.status == '404 Not Found'
    assert response.body == "{'errors': ['Not Found']}".encode('utf-8')


def test_request_to_http_error_route(application):
    # noinspection PyUnusedLocal
    def handler(request, **kwargs):
        raise BadRequestException('Missing required field "foo".')

    application.add_route(r'^/bad-request', handler)

    app = TestApp(application)

    response = app.get('/bad-request', status=400)

    assert response.status == '400 Bad Request'
    assert response.body == 'Missing required field "foo".'.encode('utf-8')


def test_request_to_unauthorized_error(application):
    # noinspection PyUnusedLocal
    def handler(request, **kwargs):
        raise UnauthorizedException('Basic', 'Test realm')

    application.add_route(r'^/unauthorized', handler)

    app = TestApp(application)
    response = app.get('/unauthorized', headers={'Accept': 'application/json'}, status=401)

    assert response.status == '401 Unauthorized'
    assert response.headers['WWW-Authenticate'] == 'Basic realm="Test realm"'
    assert response.body == b'{"errors": ["Not authorized"]}'


def test_request_to_internal_error_route(application):
    application.add_route(r'^/error', lambda r: 1 / 0)  # Division by zero

    app = TestApp(application)

    response = app.get('/error', status=500)

    assert response.status == '500 Internal Server Error'
    assert response.body == 'Internal Server Error'.encode('utf-8')


def test_request_to_internal_error_route_debug_mode(application):
    application.add_route(r'^/error', lambda r: 1 / 0)  # Division by zero
    application.debug = True

    app = TestApp(application)

    with pytest.raises(ZeroDivisionError):
        app.get('/error', status=500)


def test_application_call_handler(application, envbuilder):
    handler = Mock()
    application.add_route(r'^/(?P<arg>.*)$', handler)

    request = Request(envbuilder('GET', '/test-argument'))
    application.call_handler(request)

    handler.assert_called_once_with(request)
    assert request.path_arguments == {'arg': 'test-argument'}
