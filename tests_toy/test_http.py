import pytest
from accept import MediaType
from staty import Ok

from toy.http import Request, Response, to_title_case


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
        'Content-Length': '4',
    }
    assert repr(request) == '<Request GET />'
    assert request.content_type == 'application/json'
    assert request.charset == 'utf-8'
    assert request.accept == [MediaType('application/json')]
    assert request.accept_charset == [MediaType('iso-8859-1'), MediaType('utf-8', q=0.7)]


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