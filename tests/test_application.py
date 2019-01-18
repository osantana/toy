from unittest.mock import Mock

import pytest
from webtest import TestApp

from recipes.framework.application import Application


def test_basic_application():
    app = Application()

    assert callable(app), "It's not a WSGI middleware"
    assert app.routes == {}


@pytest.mark.parametrize('raw_path,path', [
    (r'/', r'/'),
    (r'', r'/'),
    (r'//', r'/'),
])
def test_add_normalized_route_to_application(raw_path, path):
    app = Application()
    app.add_route(raw_path, lambda req: req)
    assert len(app.routes) == 1
    assert path in app.routes


def test_basic_request_to_app(application):
    handler = Mock()
    application.add_route(r'/test', handler)

    app = TestApp(application)

    response = app.get("/test")
    assert response
