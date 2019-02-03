import json
from unittest.mock import Mock

import pytest

from toy.handlers import Handler, ResourceHandler
from toy.http import Request


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
    handler = Handler()

    handler.get = Mock()

    handler(request)

    handler.get.assert_called_once_with(request)


def test_basic_resource_handler_creation(envbuilder, basic_resource_class, json_data):
    class MyResourceHandler(ResourceHandler):
        resource_class = basic_resource_class
        route_template = '/<slug>'

    request = Request(envbuilder('POST', '/', input_stream=json_data))
    handler = MyResourceHandler()

    response = handler(request)

    assert response.status == 201
    assert response.data == json_data
    assert response.headers['Location'] == '/my-name'


@pytest.mark.skip('finish error handling at resource handler')
def test_bad_request_resource_handler_creation_missing_required_argument(envbuilder, basic_resource_class):
    class MyResourceHandler(ResourceHandler):
        resource_class = basic_resource_class
        route_template = '/<slug>'

    json_data = json.dumps({'name': 'foo'})  # missing slug
    request = Request(envbuilder('POST', '/', input_stream=json_data))
    handler = MyResourceHandler()

    response = handler(request)
    assert response.status.code == 400


def test_resource_handler_route_resolver(basic_resource_class):
    class MyResourceHandler(ResourceHandler):
        route_template = '/<slug>'

    resource = basic_resource_class.get()
    handler = MyResourceHandler()
    assert handler.get_route(resource) == '/my-name'
