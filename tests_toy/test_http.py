import pytest
from staty import Ok

from toy.http import JSONResponse, Request, Response, to_title_case


@pytest.mark.parametrize('inp,out', [
    ('HTTP_CONTENT_TYPE', 'Content-Type'),
    ('HTTP_AUTHORIZATION', 'Authorization'),
    ('HTTP_WWW_AUTHENTICATE', 'WWW-Authenticate'),
])
def test_util_upper_case_headers_to_title_case(inp, out):
    assert to_title_case(inp) == out


def test_http_basic_request(application, envbuilder, binary_content):
    env = envbuilder(
        method='GET',
        path='/',
        query_string='spam=1&eggs=2',
        input_stream=binary_content,
    )
    request = Request(application, env)

    assert request.method == 'GET'
    assert request.path == '/'
    assert request.query_string == {'spam': ['1'], 'eggs': ['2']}
    assert request.headers == {
        'Content-Type': ['application/json'],
        'Content-Length': ['4'],
    }
    assert repr(request) == '<Request GET />'


def test_http_request_lower_case_method(application, envbuilder, binary_content):
    env = envbuilder(
        method='get',
        path='/',
    )
    request = Request(application, env)
    assert request.method == 'GET'


def test_basic_basic_response():
    response = Response('Hello, World!')
    assert response.status == Ok()
    assert repr(response) == '<Response 200 OK>'


def test_response_with_extra_http_headers():
    response = Response('', ignored_arg='', http_www_authenticate='Basic realm="Test Endpoint"')
    assert response.headers['WWW-Authenticate'] == 'Basic realm="Test Endpoint"'


def test_json_response():
    response = JSONResponse(
        {
            'string': 'string',
            'number': 1,
            'boolean': True,
            'null': None,
        }
    )

    assert response.headers['Content-Type'] == 'application/json'
    assert response.data == ('{"string": "string", '
                             '"number": 1, '
                             '"boolean": true, '
                             '"null": null}')
