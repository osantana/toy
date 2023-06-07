import re

from staty import codes as status
from staty import exceptions as error_status

from . import fields
from .exceptions import ResourceNotFoundException, SerializationException, ValidationException
from .http import HTTP_METHODS, Request, Response
from .resources import Processor, Resource


class Handler:
    allowed_methods = []

    def __init__(self, methods=None, **kwargs):
        self.application_args = kwargs

        self._methods = {m.lower() for m in self.allowed_methods}

        if methods is not None:
            self._methods.update(m.lower() for m in methods)

        # exclude invalid methods
        self._methods = self._methods.intersection(m.lower() for m in HTTP_METHODS)

    def _find_handler(self, request):
        method = request.method

        if method.lower() not in self._methods:
            raise error_status.MethodNotAllowedException(f'Method {method} not allowed')

        try:
            handler = getattr(self, method.lower())
        except AttributeError:
            raise error_status.MethodNotAllowedException(f'Method {method} not allowed')
        return handler

    def authorize(self, request):
        pass

    def dispatch(self, request: Request) -> Response:
        handler = self._find_handler(request)
        self.authorize(request)
        return handler(request)

    def __call__(self, request: Request) -> Response:
        return self.dispatch(request)


class ErrorResource(Resource):
    fields = [
        fields.CharField(name='field', max_length=255, required=True),
        fields.CharField(name='message', max_length=255, required=True),
    ]


class ErrorResponseResource(Resource):
    fields = [fields.ResourceListField(name='errors', resource_type=ErrorResource)]

    def update(self, errors):
        for field_name, error_list in errors.items():
            for error in error_list:
                error_resource = ErrorResource(field=field_name, message=error.message)
                self['errors'].append(error_resource)


class ResourceHandler(Handler):
    resource_type = None
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
            status=status.BadRequest(),
        )

    def post(self, request):
        resource = self.resource_type(
            request=request,
            application_args=self.application_args,
        )

        processor = Processor(request)

        try:
            data = processor.get_data()
        except SerializationException:
            return processor.get_response(
                {'errors': [f'Invalid payload format. {request.content_type!r} expected.']},
                status=status.BadRequest(),
            )

        resource.update(data)

        try:
            response_resource = resource.create()
        except ValidationException as exc:
            return self._bad_request_error(exc, processor, request)

        headers = {
            'Location': self.get_route(response_resource),
        }

        return processor.get_response(
            data=response_resource.data,
            status=status.Created(),
            headers=headers,
        )

    def get(self, request):
        processor = Processor(request)

        try:
            resource = self.resource_type.get(
                request=request,
                application_args=self.application_args,
            )
        except ResourceNotFoundException:
            raise error_status.NotFoundException()

        except ValidationException as exc:
            return self._bad_request_error(exc, processor, request)

        return processor.get_response(
            data=resource.data,
            status=status.Ok(),
        )

    def delete(self, request):
        try:
            resource = self.resource_type(
                request=request,
                application_args=self.application_args,
            )
            response_resource = resource.remove()
        except ResourceNotFoundException:
            raise error_status.NotFoundException()

        if not response_resource:
            return Response('', status=status.NoContent(), content_type=None)

        processor = Processor(request)
        return processor.get_response(data=response_resource.data, status=status.Ok())

    def put(self, request):
        resource = self.resource_type(
            request=request,
            application_args=self.application_args,
        )

        processor = Processor(request)

        try:
            data = processor.get_data()
        except SerializationException:
            return processor.get_response(
                {'errors': [f'Invalid payload format. {request.content_type!r} expected.']},
                status=status.BadRequest(),
            )

        data_fields = set(data.keys())
        resource_fields = resource.keys(include_lazy=False)
        if resource_fields != data_fields:
            return processor.get_response(
                data={'errors': [f'Invalid resource fields {resource_fields} != {data_fields}']},
                status=status.BadRequest(),
            )

        resource.update(data)

        try:
            response_resource = resource.replace()
        except ResourceNotFoundException:
            raise error_status.NotFoundException()

        return processor.get_response(data=response_resource.data, status=status.Ok())

    def patch(self, request):
        resource = self.resource_type(
            request=request,
            application_args=self.application_args,
        )

        processor = Processor(request)

        try:
            data = processor.get_data()
        except SerializationException:
            return processor.get_response(
                {'errors': [f'Invalid payload format. {request.content_type!r} expected.']},
                status=status.BadRequest(),
            )

        try:
            response_resource = resource.change(**data)
        except ResourceNotFoundException:
            raise error_status.NotFoundException()

        return processor.get_response(data=response_resource.data, status=status.Ok())


# noinspection PyUnusedLocal
def not_found_handler(request, **kwargs):
    processor = Processor(request)
    return processor.get_response({'errors': ['Not Found']}, status.NotFound())


# noinspection PyUnusedLocal
def internal_error_handler(request, **kwargs):
    return Response('Internal Server Error', status.InternalServerError())


# noinspection PyUnusedLocal
def unauthorized_handler(request, error, **kwargs):
    headers = {
        'WWW-Authenticate': error.header,
    }
    processor = Processor(request)
    return processor.get_response({'errors': ['Not authorized']}, status=status.Unauthorized(), headers=headers)


# noinspection PyUnusedLocal
def unsupported_media_type_handler(request, error, **kwargs):
    return Response(
        f'Unsupported media type {error.media_type!r}',
        status.UnsupportedMediaType(),
        content_type='text/plain',
    )
