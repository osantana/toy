from .exceptions import ValidationError


class Validator:
    def _error(self, message, field):
        return ValidationError(message, field.name, field.value)

    def validate(self, field):
        raise NotImplementedError('Abstract class')  # pragma: nocover


class Required(Validator):
    def validate(self, field):
        if not field.value:
            return self._error('Required field', field)


class Length(Validator):
    def __init__(self, min_length=None, max_length=None):
        if min_length is not None and max_length is not None and min_length > max_length:
            raise ValueError('Invalid length specification')

        self.min_length = min_length
        self.max_length = max_length

    def validate(self, field):
        value = field.value

        if value is None:
            return

        try:
            length = len(value)
        except TypeError:
            return self._error('Value has no length', field)

        if self.max_length is not None and length > self.max_length:
            return self._error('Invalid max length', field)

        if self.min_length is not None and length < self.min_length:
            return self._error('Invalid min length', field)


class Range(Validator):
    def __init__(self, min_value=None, max_value=None):
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError('Invalid range specification')

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, field):
        value = field.value
        try:
            if self.max_value is not None and value > self.max_value:
                return self._error('Invalid max value', field)

            if self.min_value is not None and value < self.min_value:
                return self._error('Invalid min value', field)
        except TypeError:
            return self._error('Invalid value type for this field', field)


class Type(Validator):
    def __init__(self, allowed_types=None):
        if allowed_types is None:
            allowed_types = ()
        self.allowed_types = tuple(allowed_types)

    def validate(self, field):
        if field.value is None:
            return

        if not isinstance(field.value, self.allowed_types):
            return self._error(f'Invalid value type for this field', field)


class TypeList(Type):
    def validate(self, field):
        value = field.value

        if not isinstance(value, (tuple, list)):
            return self._error(f'Field must be a list or tuple', field)

        for item in value:
            if not isinstance(item, tuple(self.allowed_types)):
                return self._error(f'Invalid value type for this field', field)
