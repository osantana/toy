import re
from urllib.parse import parse_qs

from staty import Ok


def upper_case_to_title_case(upper):
    upper = re.sub(r'^HTTP_', '', upper.upper())

    splitted = [(w if w == 'WWW' else w.title()) for w in upper.split('_')]

    return '-'.join(splitted)


class Request:
    def __init__(self, environ):
        self.method = environ.get('REQUEST_METHOD', 'GET')
        self.path = environ.get('PATH_INFO', '/')

        query_string = environ.get('QUERY_STRING', '')
        self.query_string = parse_qs(query_string)

        headers = {}
        for key, value in environ.items():
            if not key.startswith('HTTP_'):
                continue

            key = upper_case_to_title_case(key)

            if key in headers:
                headers[key].append(value)
            else:
                headers[key] = [value]

        self.headers = headers


class Response:
    def __init__(self, data, status=Ok(), headers=None, **kwargs):
        self.status = status

        if headers is None:
            headers = {}
        self.headers = headers

        self.data = data
