import re
from urllib.parse import parse_qs

import accept
from staty import Ok


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
    def __init__(self, application, environ):
        self.application = application
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
    def __init__(self, data: str, status=Ok(), headers=None,
                 content_type='application/octet-stream', **kwargs):
        self.status = status

        if headers is None:
            headers = {}
        self.headers = headers

        self.data = data

        self.headers['Content-Type'] = content_type

        for key, value in kwargs.items():
            if not key.startswith('http_'):
                continue

            self.headers[to_title_case(key)] = value

    def __repr__(self):
        return f'<Response {str(self.status)}>'


class WSGIResponse:
    def __init__(self, response: Response, charset='utf-8') -> None:
        self.response = response
        self.charset = charset

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
        return [self.response.data.encode(self.charset)]
