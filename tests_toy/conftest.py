from io import BytesIO

import pytest
from webtest import TestApp

from toy.application import Application
from toy.http import Response


@pytest.fixture
def application():
    app = Application()
    app.add_route(r'^/$', lambda req: req)
    return app


@pytest.fixture
def client(application):
    return TestApp(application)


def _environ_builder(method, path, input_stream=None, **kwargs):
    if input_stream is None:
        input_stream = BytesIO()

    if isinstance(input_stream, str):
        input_stream = BytesIO(input_stream.encode('iso-8859-1'))

    if isinstance(input_stream, bytes):
        input_stream = BytesIO(input_stream)

    start_pos = input_stream.tell()
    input_stream.seek(0, 2)
    end_pos = input_stream.tell()
    input_stream.seek(start_pos)
    content_length = end_pos - start_pos

    result = {
        'REQUEST_METHOD': method.upper(),
        'PATH_INFO': path,
        'QUERY_STRING': kwargs.get('query_string', ''),
        'ACCEPT': kwargs.get('accept', 'application/json'),
        'ACCEPT_CHARSET': kwargs.get('accept_charset', 'iso-8859-1, utf-8;q=0.7'),
        'CONTENT_TYPE': kwargs.get('content_type', 'application/json; charset=iso-8859-1'),
        'CONTENT_LENGTH': str(content_length),
        'wsgi.input': input_stream,
    }

    result['HTTP_ACCEPT'] = result['ACCEPT']
    result['HTTP_ACCEPT_CHARSET'] = result['ACCEPT_CHARSET']
    result['HTTP_CONTENT_TYPE'] = result['CONTENT_TYPE']
    result['HTTP_CONTENT_LENGTH'] = result['CONTENT_LENGTH']

    if 'authorization' in kwargs:
        result['HTTP_AUTHORIZATION'] = kwargs['authorization']

    return result


@pytest.fixture
def envbuilder():
    return _environ_builder


@pytest.fixture
def binary_content():
    content = BytesIO()
    content.write(b'Test')
    content.seek(0)
    return content


@pytest.fixture
def handler():
    # noinspection PyUnusedLocal
    def _hello(request, **kwargs):
        return Response('Hello!', content_type='text/plain; charset=utf-8')
    return _hello
