from webtest import TestApp

from recipes.framework.application import Application


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
