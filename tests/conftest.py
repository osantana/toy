from io import BytesIO

import pytest
from webtest import TestApp

from recipes.framework.application import Application


@pytest.fixture
def application():
    app = Application()
    app.add_route(r'/', lambda req: req)
    return app


@pytest.fixture
def client(application):
    return TestApp(application)


def _environ_builder(method, path, input_stream, **kwargs):
    start_pos = input_stream.tell()
    input_stream.seek(0, 2)
    end_pos = input_stream.tell()
    input_stream.seek(start_pos)
    content_length = end_pos - start_pos

    result = {
        'REQUEST_METHOD': method.upper(),
        'PATH_INFO': path,
        'QUERY_STRING': kwargs.get('query_string', ''),
        'CONTENT_TYPE': kwargs.get('content_type', 'application/json'),
        'CONTENT_LENGTH': str(content_length),
        'wsgi.input': input_stream,
    }

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
