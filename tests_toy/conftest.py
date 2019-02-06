import json
from io import BytesIO

import pytest

from toy import fields
from toy.application import Application
from toy.handlers import Handler
from toy.http import Request, Response
from toy.resources import Resource


@pytest.fixture
def application():
    app = Application()
    app.add_route(r'^/$', lambda req: req)
    return app


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
def hello_response():
    return Response('Hello!', content_type='text/plain; charset=utf-8')


@pytest.fixture
def handler(hello_response):
    # noinspection PyUnusedLocal
    def _hello(request, **kwargs):
        return hello_response

    return _hello


@pytest.fixture
def get_handler(hello_response):
    class GetHandler(Handler):
        allowed_methods = ['get']

        # noinspection PyUnusedLocal
        def get(self, request):
            hello_response.data = 'Hello GET!'
            return hello_response

    return GetHandler()


@pytest.fixture
def post_handler(hello_response):
    class PostHandler(Handler):
        allowed_methods = ['post']

        # noinspection PyUnusedLocal
        def post(self, request):
            hello_response.data = 'Hello POST!'
            return hello_response

    return PostHandler()


@pytest.fixture
def basic_resource_class():
    # noinspection PyAbstractClass
    class MyResource(Resource):
        fields = [
            fields.CharField(name='name', max_length=255, required=True),
            fields.CharField(name='description', max_length=255),
            fields.CharField(name='slug', max_length=255, required=True, lazy=True),
        ]

        @classmethod
        def do_get(cls, request=None, application_args=None):
            resource = cls(request=request, application_args=application_args)
            resource.update({
                'name': 'My Name',
                'description': 'My Description',
                'slug': 'my-name',
            })
            return resource

        def do_create(self):
            pass

    return MyResource


@pytest.fixture
def resource(basic_resource_class):
    return basic_resource_class()


@pytest.fixture
def json_data():
    json_str = '''
      {
        "name": "My Name",
        "description": "My Description",
        "slug": "my-name"
      }
    '''.strip()
    return json.dumps(json.loads(json_str))  # strip blanks


@pytest.fixture
def post_request(envbuilder):
    data = {
        'name': 'My Name',
        'description': 'My Description',
        'slug': 'my-name',
    }
    environ = envbuilder(
        method='POST',
        path='/',
        content_type='application/json',
        input_stream=json.dumps(data),
    )
    return Request(environ)


@pytest.fixture
def component_resource_class():
    class MyResourceItem(Resource):
        fields = [
            fields.CharField(name='name', max_length=255),
        ]

    return MyResourceItem


@pytest.fixture
def composite_resource_class(component_resource_class):
    class MyResource(Resource):
        fields = [
            fields.CharField(name='name', max_length=255),
            fields.ResourceField(name='sub_item', resource_type=component_resource_class),
            fields.ResourceListField(name='items', resource_type=component_resource_class),
        ]

    return MyResource


@pytest.fixture
def compound_resource(composite_resource_class):
    data = {
        'name': 'My Resource',
        'sub_item': {
            'name': 'My Individual Sub Resource',
        },
        'items': [
            {'name': 'My Resource Item #1'},
            {'name': 'My Resource Item #2'},
            {'name': 'My Resource Item #3'},
        ],
    }
    resource = composite_resource_class()
    resource.update(data)
    return resource
