from typing import Optional
from uuid import UUID

from .exceptions import ValidationError
from .resources import Resource


# TODO:
#  - support for datetime field
#  - support for date field
#  - support for time field
#  - support for timedelta field

class Validator:
    def validate(self, field):
        raise NotImplementedError('Abstract class')  # pragma: nocover


class Required(Validator):
    def validate(self, field):
        if not field.value:
            raise ValidationError(f'Field {field.name} is required')


class Field:
    def __init__(self, name, lazy=False, validators=None):
        self.name = name
        self.lazy = lazy

        if validators is None:
            validators = []
        else:
            for validator in validators:
                if not isinstance(validator, Validator):
                    raise TypeError('Invalid validator')

        self.validators = validators

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
            return

        self._old_value = self._value
        self._value = new_value

    def validate(self, include_lazy=True):
        if not include_lazy and self.lazy:
            return

        for validator in self.validators:
            validator.validate(self)

    def clean(self):
        self._old_value = self.value

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        return self._value == other


class UUIDField(Field):
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, UUID):
            raise ValueError('Invalid UUID value')

        super(UUIDField, self.__class__).value.fset(self, new_value)


class CharField(Field):
    def __init__(self, name, max_length, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.max_length = max_length

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, new_value):
        if len(new_value) > self.max_length:
            raise ValueError(f'Invalid string length ({len(new_value)} > {self.max_length})')

        super(CharField, self.__class__).value.fset(self, new_value)


class IntegerField(Field):
    def __init__(self, name, min_value: Optional[int] = None, max_value: Optional[int] = None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        if min_value and max_value and min_value > max_value:
            raise ValueError('Invalid values range for integer')

        self.min_value = min_value
        self.max_value = max_value

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, new_value):
        if any((self.max_value and new_value > self.max_value, self.min_value and new_value < self.min_value)):
            raise ValueError(f'Invalid integer value ({self.min_value} > {new_value} > {self.max_value})')

        if not isinstance(new_value, int):
            raise TypeError('Invalid integer value type')

        super(IntegerField, self.__class__).value.fset(self, new_value)


class BooleanField(Field):
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, bool):
            raise ValueError('Invalid boolean value')

        super(BooleanField, self.__class__).value.fset(self, new_value)


class _ResourceFieldBase(Field):
    def __init__(self, name, resource_type, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        if not issubclass(resource_type, Resource):
            raise TypeError('Invalid resource type')

        self.resource_type = resource_type


class ResourceField(_ResourceFieldBase):
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, self.resource_type):
            raise TypeError('Invalid resource type')

        super(ResourceField, self.__class__).value.fset(self, new_value)


class ResourceListField(_ResourceFieldBase):
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, (tuple, list)):
            raise TypeError('Invalid list value')

        for item in new_value:
            if not isinstance(item, self.resource_type):
                raise TypeError('Invalid resource type inside list')

        super(ResourceListField, self.__class__).value.fset(self, new_value)
