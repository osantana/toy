from staty import InternalServerError, MethodNotAllowedException, NotFound

from .http import Request, Response


class Handler:
    def dispatch(self, request: Request, **kwargs) -> Response:
        method = request.method

        try:
            handler = getattr(self, method.lower())
        except AttributeError:
            raise MethodNotAllowedException(f'Method {method} not allowed')

        return handler(request)

    def __call__(self, request):
        return self.dispatch(request)


# noinspection PyUnusedLocal
def not_found_handler(request, **kwargs):
    return Response(f'URL {request.path} not found.', NotFound())


# noinspection PyUnusedLocal
def internal_error_handler(request, **kwargs):
    return Response("Internal Server Error", InternalServerError())
