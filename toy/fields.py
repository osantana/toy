from typing import Optional
from uuid import UUID

from toy.exceptions import ValidationError, ValidationException
from .resources import Resource


# TODO:
#  - support for datetime field
#  - support for date field
#  - support for time field
#  - support for timedelta field


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
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, field):
        try:
            length = len(field.value)
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
        self.allowed_types = allowed_types

    def validate(self, field):
        if not isinstance(field.value, tuple(self.allowed_types)):
            return self._error(f'Invalid value type for this field', field)


class TypeList(Type):
    def validate(self, field):
        value = field.value

        if not isinstance(value, (tuple, list)):
            return self._error(f'Field must be a list or tuple', field)

        for item in value:
            if not isinstance(item, tuple(self.allowed_types)):
                return self._error(f'Invalid value type for this field', field)


class Field:
    default_validators = []

    def __init__(self, name, lazy=False, validators=None):
        self.name = name
        self.lazy = lazy

        self.validators = self.default_validators[:]
        if validators is not None:
            for validator in validators:
                if not isinstance(validator, Validator):
                    raise TypeError('Invalid validator')
                self.validators.append(validator)

        self._old_value = None
        self._value = None

    @property
    def dirty(self):
        return self.value != self.old_value

    @property
    def old_value(self):
        return self._old_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == self._value:
            return

        if new_value == self._old_value:
            self._value = self.old_value
            return

        self._old_value = self._value
        self._value = new_value

    def validate(self, include_lazy=True, raise_exception=False):
        if not include_lazy and self.lazy:
            return

        errors = []
        for validator in self.validators:
            error = validator.validate(self)
            if not error:
                continue
            errors.append(error)

        if raise_exception and errors:
            raise ValidationException('Validation Error', errors=errors)

        return errors

    def clean(self):
        self._old_value = self.value

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        return self._value == other


class UUIDField(Field):
    default_validators = [Type([UUID])]


class CharField(Field):
    default_validators = [Type([str])]

    def __init__(self, name, max_length, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.validators.append(Length(max_length=max_length))


class IntegerField(Field):
    default_validators = [Type([int])]

    def __init__(self, name, min_value: Optional[int] = None, max_value: Optional[int] = None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.validators.append(Range(min_value=min_value, max_value=max_value))


class BooleanField(Field):
    default_validators = [Type([bool])]


class ResourceField(Field):
    def __init__(self, name, resource_type, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        if not issubclass(resource_type, Resource):
            raise TypeError('Invalid resource type')

        self.validators.append(Type([resource_type]))


class ResourceListField(Field):
    def __init__(self, name, resource_type, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        if not issubclass(resource_type, Resource):
            raise TypeError('Invalid resource type')

        self.resource_type = resource_type
        self.validators.append(TypeList([resource_type]))
