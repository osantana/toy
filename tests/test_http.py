import pytest
from staty import Ok

from recipes.framework.http import Request, Response, to_title_case


@pytest.mark.parametrize('inp,out', [
    ('HTTP_CONTENT_TYPE', 'Content-Type'),
    ('HTTP_AUTHORIZATION', 'Authorization'),
    ('HTTP_WWW_AUTHENTICATE', 'WWW-Authenticate'),
])
def test_util_upper_case_headers_to_title_case(inp, out):
    assert to_title_case(inp) == out


def test_http_basic_request(envbuilder, binary_content):
    env = envbuilder(
        method='GET',
        path='/',
        query_string='spam=1&eggs=2',
        input_stream=binary_content,
    )
    request = Request(env)

    assert request.method == 'GET'
    assert request.path == '/'
    assert request.query_string == {'spam': ['1'], 'eggs': ['2']}
    assert request.headers == {
        'Content-Type': ['application/json'],
        'Content-Length': ['4'],
    }


def test_http_request_lower_case_method(envbuilder, binary_content):
    env = envbuilder(
        method='get',
        path='/',
    )
    request = Request(env)
    assert request.method == 'GET'


def test_basic_basic_response():
    response = Response('Hello, World!')
    assert response.status == Ok()


def test_response_with_extra_http_headers():
    response = Response('', ignored_arg='', http_www_authenticate='Basic realm="Test Endpoint"')
    assert response.headers['WWW-Authenticate'] == 'Basic realm="Test Endpoint"'
