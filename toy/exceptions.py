class ToyException(Exception):
    pass


class InvalidRouteHandler(ToyException):
    pass


class ValidationError(ToyException):
    pass
