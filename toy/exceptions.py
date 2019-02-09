class ToyException(Exception):
    pass


class InvalidRouteHandler(ToyException):
    pass


# Validation Error System for Resource and Fields
class ValidationError:
    def __init__(self, message, name, value):
        self.message = message
        self.name = name
        self.value = value

    def __repr__(self):
        return f'<ValidationError {self.message} {self.name!r} {self.value!r}>'


class ValidationException(ToyException):
    def __init__(self, message, errors, *args):
        super().__init__(message, *args)
        self.errors = errors


class ResourceNotFound(ToyException):
    pass
