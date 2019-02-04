import re

from staty import BadRequest, Created, InternalServerError, MethodNotAllowedException, NotFound

from . import fields
from .exceptions import ValidationException
from .http import HTTP_METHODS, Request, Response
from .resources import Processor, Resource


class Handler:
    def __init__(self, **kwargs):
        self.application_args = kwargs

    def _find_handler(self, request):
        method = request.method

        if method not in HTTP_METHODS:
            raise MethodNotAllowedException(f'Method {method} not allowed')

        try:
            handler = getattr(self, method.lower())
        except AttributeError:
            raise MethodNotAllowedException(f'Method {method} not allowed')
        return handler

    def dispatch(self, request: Request) -> Response:
        handler = self._find_handler(request)
        return handler(request)

    def __call__(self, request: Request) -> Response:
        return self.dispatch(request)


class ErrorResource(Resource):
    fields = [
        fields.CharField(name='message', max_length=255, required=True),
    ]


class ErrorResponseResource(Resource):
    fields = [
        fields.ResourceListField(name='errors', resource_type=ErrorResource)
    ]

    def update(self, errors):
        print(errors)


class ResourceHandler(Handler):
    resource_class = None
    error_response_resource_class = ErrorResponseResource
    route_template = ''

    def get_route(self, resource: Resource):
        route_args = set(re.findall(r'<(.*?)>', self.route_template))
        route = self.route_template
        for arg in route_args:
            value = None
            try:
                attr = getattr(self, arg)
                if callable(attr):
                    value = attr(resource)
            except AttributeError:
                value = resource.data[arg]

            route = route.replace(f'<{arg}>', f'{value}')

        return route

    def _bad_request_error(self, exc, processor, request):
        resource = self.error_response_resource_class(
            request=request,
            application_args=self.application_args,
        )
        resource.update(exc.errors)
        return processor.get_response(
            data=resource.data,
            status=BadRequest(),
        )

    def post(self, request):
        resource = self.resource_class(
            request=request,
            application_args=self.application_args,
        )

        processor = Processor(request)
        data = processor.get_data()

        resource.update(data)

        try:
            resource.create()
        except ValidationException as exc:
            return self._bad_request_error(exc, processor, request)

        headers = {
            'Location': self.get_route(resource),
        }

        return processor.get_response(
            data=resource.data,
            status=Created(),
            headers=headers,
        )


# noinspection PyUnusedLocal
def not_found_handler(request, **kwargs):
    return Response(f'URL {request.path} not found.', NotFound())


# noinspection PyUnusedLocal
def internal_error_handler(request, **kwargs):
    return Response("Internal Server Error", InternalServerError())
