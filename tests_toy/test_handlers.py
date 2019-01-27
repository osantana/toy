from unittest.mock import Mock

import pytest
from staty import MethodNotAllowedException

from toy.handlers import Handler
from toy.http import Request


def test_basic_dispatcher_handler(application, envbuilder):
    request = Request(envbuilder("GET", "/test"))
    handler = Handler(application)

    mock = Mock()
    handler.dispatch = mock

    handler(request)

    mock.assert_called_once_with(request)


def test_basic_allowed_method_call(application, envbuilder):
    request = Request(envbuilder("GET", "/test"))
    handler = Handler(application)

    handler.get = Mock()

    handler(request)

    handler.get.assert_called_once_with(request)


def test_error_not_allowed_method_call(application, envbuilder):
    request = Request(envbuilder("POST", "/test"))
    handler = Handler(application)

    handler.get = Mock()

    with pytest.raises(MethodNotAllowedException):
        handler(request)
