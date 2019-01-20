from staty import MethodNotAllowedException

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
