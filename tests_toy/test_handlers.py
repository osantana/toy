from unittest.mock import Mock

import pytest

from toy.handlers import Handler, ResourceHandler
from toy.http import Request


def test_basic_handler_arguments():
    handler = Handler(arg='value')
    assert handler.arguments == {'arg': 'value'}


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


def test_dispatch_handler_arguments_to_method(envbuilder):
    request = Request(envbuilder('GET', '/test'))
    handler = Handler(arg='value')

    handler.get = Mock()
    handler(request)

    handler.get.assert_called_once_with(request, arg='value')


@pytest.mark.skip('TODO: finish this test')
def test_basic_resource_handler_creation(envbuilder, basic_resource_class, json_data):
    class MyResourceHandler(ResourceHandler):
        resource_class = basic_resource_class

    request = Request(envbuilder('POST', '/', input_stream=json_data))
    handler = MyResourceHandler()

    response = handler(request)

    assert response.status == 201
    assert response.data == json_data
