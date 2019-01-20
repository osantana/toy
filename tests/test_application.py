from unittest.mock import Mock

from webtest import TestApp

from recipes.framework.application import Application
from recipes.framework.http import Request


def test_basic_application():
    app = Application()

    assert callable(app), "It's not a WSGI middleware"
    assert len(app.routes) == 0


def test_basic_request_to_app(application, handler):
    application.add_route(r'^/test', handler)

    app = TestApp(application)

    response = app.get("/test")

    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'text/plain'
    assert response.body == 'Hello!'.encode('utf-8')


def test_application_call_handler(application, envbuilder):
    handler = Mock()
    application.add_route(r'^/(?P<arg>.*)$', handler)

    request = Request(envbuilder('GET', '/test-argument'))
    application.call_handler(request)

    handler.assert_called_once_with(request, arg='test-argument')
