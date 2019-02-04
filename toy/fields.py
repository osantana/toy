from typing import Optional
from uuid import UUID

from .exceptions import ValidationException
from .validators import Validator, Required, Length, Range, Type, TypeList
from .resources import Resource


# TODO:
#  - support for datetime field
#  - support for date field
#  - support for time field
#  - support for timedelta field


class Field:
    default_validators = []

    def __init__(self, name, required=False, lazy=False, validators=None):
        self.name = name
        self.lazy = lazy

        self.validators = self.default_validators[:]
        if validators is not None:
            for validator in validators:
                if not isinstance(validator, Validator):
                    raise TypeError('Invalid validator')
                self.validators.append(validator)

        if required:
            self.validators.append(Required())

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
