from typing import Optional
from uuid import UUID

from .resources import Resource


# TODO:
#  - support for validators (ex. required)
#  - support for dirt/clean fields
#  - support for lazy field validator (like id)?

class Field:
    def __init__(self, name):
        self.name = name
        self._value = None

    @property
    def value(self):
        raise NotImplementedError('Field is an abstract class')  # pragma: nocover

    @value.setter
    def value(self, new_value):
        raise NotImplementedError('Field is an abstract class')  # pragma: nocover

    def __eq__(self, other):
        return self._value == other


class UUIDField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, UUID):
            raise ValueError('Invalid UUID value')

        self._value = new_value


class CharField(Field):
    def __init__(self, name, max_length):
        super().__init__(name)
        self.max_length = max_length

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if len(new_value) > self.max_length:
            raise ValueError(f'Invalid string length ({len(new_value)} > {self.max_length})')

        self._value = new_value


class IntegerField(Field):
    def __init__(self, name, min_value: Optional[int] = None, max_value: Optional[int] = None):
        super().__init__(name)

        if min_value and max_value and min_value > max_value:
            raise ValueError('Invalid values range for integer')

        self.min_value = min_value
        self.max_value = max_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if any((self.max_value and new_value > self.max_value, self.min_value and new_value < self.min_value)):
            raise ValueError(f'Invalid integer value ({self.min_value} > {new_value} > {self.max_value})')

        if not isinstance(new_value, int):
            raise TypeError('Invalid integer value type')

        self._value = new_value


class BooleanField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, bool):
            raise ValueError('Invalid boolean value')
        self._value = new_value


class ResourceField(Field):
    def __init__(self, name, resource_type):
        super().__init__(name)

        if not issubclass(resource_type, Resource):
            raise TypeError('Invalid resource type')

        self.resource_type = resource_type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, self.resource_type):
            raise TypeError('Invalid resource type')
        self._value = new_value


class ResourceListField(ResourceField):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, (tuple, list)):
            raise TypeError('Invalid list value')

        for item in new_value:
            if not isinstance(item, self.resource_type):
                raise TypeError('Invalid resource type inside list')

        self._value = new_value
