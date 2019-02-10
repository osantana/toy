class ToyException(Exception):
    pass


class InvalidRouteHandlerException(ToyException):
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


class ResourceNotFoundException(ToyException):
    pass


class UnauthorizedException(ToyException):
    def __init__(self, auth_type, realm='', charset=False):
        self.auth_type = auth_type.title()
        self.realm = realm
        self.charset = 'UTF-8' if charset else charset

    @property
    def header(self):
        head = f'{self.auth_type}'
        if self.realm:
            realm = self.realm.replace('"', r'\"')
            head = head + f' realm="{realm}"'
        if self.charset:
            head = head + f', charset="{self.charset}"'
        return head
