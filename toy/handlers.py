from staty import MethodNotAllowedException, NotFound, InternalServerError

from .http import Request, Response


class Handler:
    def dispatch(self, request: Request, **kwargs) -> Response:
        method = request.method

        try:
            handler = getattr(self, method.lower())
        except AttributeError:
            raise MethodNotAllowedException(f'Method {method} not allowed')

        return handler(request, **kwargs)

    def __call__(self, request, **kwargs):
        return self.dispatch(request, **kwargs)


# noinspection PyUnusedLocal
def not_found_handler(request, **kwargs):
    return Response(f'URL {request.path} not found.', NotFound())


# noinspection PyUnusedLocal
def internal_error_handler(request, **kwargs):
    return Response("Internal Server Error", InternalServerError())
