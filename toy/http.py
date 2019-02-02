import re
from io import BytesIO
from urllib.parse import parse_qs

import accept
from staty import HTTPStatus, Ok

HTTP_METHODS = {
    'PATCH',
    'CONNECT',
    'DELETE',
    'GET',
    'OPTIONS',
    'HEAD',
    'POST',
    'PUT',
    'TRACE',
}


def to_title_case(text):
    text = text.upper()
    text = re.sub(r'^HTTP_', '', text)
    splitted = [(w if w == 'WWW' else w.title()) for w in text.split('_')]
    return '-'.join(splitted)


def parse_content_type(content_type, default_charset='iso-8859-1'):
    content_type = content_type.lower()
    charset = default_charset

    content_type_args = content_type.split(';')
    for arg in content_type_args:
        arg = arg.strip()
        if arg.startswith('charset='):
            charset = arg.replace('charset=', '', 1)

    return content_type_args[0], charset


class Request:
    def __init__(self, environ):
        self.method = environ.get('REQUEST_METHOD', 'GET').upper()
        self.path = environ.get('PATH_INFO', '/')

        query_string = environ.get('QUERY_STRING', '')
        self.query_string = parse_qs(query_string)

        headers = {}
        for key, value in environ.items():
            if not key.startswith('HTTP_'):
                continue

            key = to_title_case(key)
            headers[key] = value

        self.headers = headers

        content_type = self.headers.pop('Content-Type', 'application/octet-stream')
        content_type, charset = parse_content_type(content_type)

        self.content_type = content_type
        self.charset = charset

        self.accept = accept.parse(self.headers.pop('Accept', 'application/octet-stream'))
        accept_charset = self.headers.pop('Accept-Charset', 'iso-8859-1, utf-8;q=0.7').lower()
        self.accept_charset = accept.parse(accept_charset)

        self.args = {}

        self.content_stream = environ['wsgi.input']
        self.content_stream.seek(0)
        self._cached_data = ""

    @property
    def data(self):
        if not self._cached_data:
            prev = self.content_stream.tell()
            self.content_stream.seek(0)
            content = self.content_stream.read()
            self.content_stream.seek(prev)
            self._cached_data = content.decode(self.charset)
        return self._cached_data

    def __repr__(self):
        return f'<Request {self.method} {self.path}>'


class Response:
    def __init__(self, data: str, status: HTTPStatus = None, headers=None,
                 content_type='application/octet-stream; charset=iso-8859-1', **kwargs):

        if status is None:
            status = Ok()

        self.status = status
        self.data = data

        if headers is None:
            headers = {}
        self.headers = headers

        for key, value in kwargs.items():
            if not key.startswith('http_'):
                continue

            self.headers[to_title_case(key)] = value

        content_type, charset = parse_content_type(content_type)
        self.content_type = content_type
        self.charset = charset

        self.headers['Content-Type'] = f'{content_type}; charset={charset}'

    @property
    def content_stream(self):
        return BytesIO(self.data.encode(self.charset))

    def __repr__(self):
        return f'<Response {str(self.status)}>'


class WSGIResponse:
    def __init__(self, response: Response) -> None:
        self.response = response

    @property
    def status(self) -> str:
        return str(self.response.status)

    @property
    def headers(self) -> list:
        headers = []
        for key, value in self.response.headers.items():
            headers.append((key, value))
        return headers

    @property
    def body(self):
        return [self.response.content_stream.read()]
