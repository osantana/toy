import json
from unittest.mock import Mock

import pytest

from toy.exceptions import UnauthorizedException
from toy.handlers import Handler, ResourceHandler
from toy.http import Request
from toy.staty import MethodNotAllowedException


def test_basic_handler_arguments():
    handler = Handler(arg='value')
    assert handler.application_args == {'arg': 'value'}


def test_basic_dispatcher_handler(envbuilder):
    request = Request(envbuilder('GET', '/test'))
    handler = Handler()

    mock = Mock()
    handler.dispatch = mock

    handler(request)

    mock.assert_called_once_with(request)


def test_basic_allowed_method_call(envbuilder):
    request = Request(envbuilder('GET', '/test'))
    handler = Handler(methods=['get'])

    handler.authorize = Mock()
    handler.get = Mock()

    handler(request)

    handler.authorize.assert_called_once_with(request)
    handler.get.assert_called_once_with(request)


def test_fail_allowed_but_not_implemented_method(envbuilder):
    request = Request(envbuilder('GET', '/test'))
    handler = Handler(methods=['get'])

    with pytest.raises(MethodNotAllowedException):
        handler(request)


def test_basic_resource_handler_creation(envbuilder, basic_resource_class, json_data):
    class MyResourceHandler(ResourceHandler):
        allowed_methods = ['post']
        resource_type = basic_resource_class
        route_template = '/<slug>'

    request = Request(envbuilder('POST', '/', input_stream=json_data))
    handler = MyResourceHandler()

    response = handler(request)

    assert response.status == 201
    assert response.data == json_data
    assert response.headers['Location'] == '/my-name'


def test_bad_request_resource_handler_creation_missing_required_argument(envbuilder, basic_resource_class):
    class MyResourceHandler(ResourceHandler):
        allowed_methods = ['post']
        resource_type = basic_resource_class
        route_template = '/<slug>'

    json_data = json.dumps({'name': 'foo'})  # missing slug
    request = Request(envbuilder('POST', '/', input_stream=json_data))
    handler = MyResourceHandler()

    expected_error = json.dumps(json.loads("""
        {
          "errors": [
            {"field": "slug", "message": "Required field"}
          ]
        }
    """))

    response = handler(request)
    assert response.status.code == 400
    assert response.data == expected_error


def test_resource_handler_route_resolver(basic_resource_class):
    class MyResourceHandler(ResourceHandler):
        route_template = '/<get_id>/<slug>'

        def get_id(self, _):
            return 'id'

    resource = basic_resource_class.get()
    handler = MyResourceHandler()
    assert handler.get_route(resource) == '/id/my-name'


def test_authorized_request(envbuilder):
    request = Request(envbuilder('GET', '/test'))
    handler = Handler(methods=['get'])

    handler.authorize = Mock()
    handler.get = Mock()

    handler(request)

    handler.authorize.assert_called_once_with(request)
    handler.get.assert_called_once_with(request)


def test_fail_not_authorized_request(envbuilder):
    request = Request(envbuilder('GET', '/test'))
    handler = Handler(methods=['get'])
    handler.authorize = Mock(side_effect=UnauthorizedException('basic'))
    handler.get = Mock()

    with pytest.raises(UnauthorizedException):
        handler(request)


def test_authenticate_header():
    error = UnauthorizedException('basic')
    assert error.header == 'Basic'

    error = UnauthorizedException('basic', 'Access to the staging site')
    assert error.header == 'Basic realm="Access to the staging site"'

    error = UnauthorizedException('basic', 'Escape "double quote"')
    assert error.header == r'Basic realm="Escape \"double quote\""'

    error = UnauthorizedException('basic', 'Access to the staging site', charset=True)
    assert error.header == 'Basic realm="Access to the staging site", charset="UTF-8"'
