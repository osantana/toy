from staty import InternalServerError, MethodNotAllowedException, NotFound, Created

from .resources import Processor
from .http import HTTP_METHODS, Request, Response


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


class ResourceHandler(Handler):
    resource_class = None

    def post(self, request):
        resource = self.resource_class(
            request=request,
            application_args=self.application_args,
        )

        processor = Processor(request)
        data = processor.get_data()

        resource.update(data)
        resource.create()

        # TODO: Location header

        return processor.get_response(
            data=resource.data,
            status=Created(),
        )


# noinspection PyUnusedLocal
def not_found_handler(request, **kwargs):
    return Response(f'URL {request.path} not found.', NotFound())


# noinspection PyUnusedLocal
def internal_error_handler(request, **kwargs):
    return Response("Internal Server Error", InternalServerError())
