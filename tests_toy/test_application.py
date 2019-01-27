from unittest.mock import Mock

import pytest
from staty import BadRequestException
from webtest import TestApp

from toy.application import Application
from toy.http import Request


def test_basic_application():
    app = Application()

    assert callable(app), "It's not a WSGI middleware"
    assert len(app.routes) == 0
    assert len(app.extensions) == 0


def test_basic_request_to_app(application, handler):
    application.add_route(r'^/test', handler)

    app = TestApp(application)

    response = app.get('/test')

    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'text/plain'
    assert response.body == 'Hello!'.encode('utf-8')


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
    assert response.body == 'URL /not-found not found.'.encode('utf-8')


def test_request_to_http_error_route(application):
    # noinspection PyUnusedLocal
    def handler(request, **kwargs):
        raise BadRequestException('Missing required field "foo".')

    application.add_route(r'^/bad-request', handler)

    app = TestApp(application)

    response = app.get('/bad-request', status=400)

    assert response.status == '400 Bad Request'
    assert response.body == 'Missing required field "foo".'.encode('utf-8')


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

    request = Request(application, envbuilder('GET', '/test-argument'))
    application.call_handler(request)

    handler.assert_called_once_with(request)
    assert request.args == {'arg': 'test-argument'}
