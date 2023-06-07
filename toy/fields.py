from uuid import UUID

from .exceptions import ValidationException
from .resources import Resource
from .validators import Length, Range, Required, Type, TypeList, Validator


class Field:
    default_validators = []

    def __init__(self, name, lazy=False, required=False, validators=None, *args, **kwargs):
        self.name = name
        self.lazy = lazy
        self.validators = []
        self.required = required

        self._load_validators(validators)

        self._old_value = None
        self._value = None

        self.request = None
        self.application_args = None

        self._args = args
        self._kwargs = kwargs

    def _load_validators(self, validators):
        self.validators = self.default_validators[:]

        if self.required:
            self.validators.append(Required())

        if validators is None:
            return

        for validator in validators:
            if not isinstance(validator, Validator):
                raise TypeError('Invalid validator')
            self.validators.append(validator)

    def copy(self):
        field = self.__class__(
            name=self.name,
            lazy=self.lazy,
            required=self.required,
            *self._args,
            **self._kwargs,
        )
        field.validators = self.validators[:]
        return field

    def _get_data(self):
        return self.value

    @property
    def data(self):
        return self._get_data()

    @property
    def dirty(self):
        return self.value != self.old_value

    @property
    def old_value(self):
        return self._old_value

    def _set_value(self, new_value):
        if new_value == self._value:
            return

        if new_value == self._old_value:
            self._value = self.old_value
            return

        self._old_value = self._value
        self._value = new_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._set_value(new_value)

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

    def _get_data(self):
        if self.value is None:
            return
        return str(self.value)


class CharField(Field):
    default_validators = [Type([str])]

    def __init__(self, name, max_length, *args, **kwargs):
        super().__init__(name, max_length=max_length, *args, **kwargs)
        self.validators.append(Length(max_length=max_length))


class IntegerField(Field):
    default_validators = [Type([int])]

    def __init__(self, name, min_value: int | None = None, max_value: int | None = None, *args, **kwargs):
        super().__init__(name, min_value=min_value, max_value=max_value, *args, **kwargs)
        self.validators.append(Range(min_value=min_value, max_value=max_value))


class BooleanField(Field):
    default_validators = [Type([bool])]


class ResourceField(Field):
    def __init__(self, name, resource_type, *args, **kwargs):
        super().__init__(name, resource_type=resource_type, *args, **kwargs)

        if not issubclass(resource_type, Resource):
            raise TypeError('Invalid resource type')

        self.validators.append(Type([resource_type]))

        self.resource_type = resource_type

    def _set_value(self, new_value):
        if isinstance(new_value, Resource):
            return super()._set_value(new_value)  # to be .validate()'d

        resource = self.resource_type(
            request=self.request,
            application_args=self.application_args,
        )
        resource.update(new_value)
        super()._set_value(resource)

    def _get_data(self):
        if self.value is None:
            return
        return self.value.data


class ResourceListField(Field):
    def __init__(self, name, resource_type, *args, **kwargs):
        super().__init__(name, resource_type=resource_type, *args, **kwargs)

        if not issubclass(resource_type, Resource):
            raise TypeError('Invalid resource type')

        self.validators.append(TypeList([resource_type]))

        self.resource_type = resource_type
        self._value = []

    def _set_value(self, new_value):
        if not isinstance(new_value, list | tuple):
            return super()._set_value(new_value)  # to be .validate()'d

        resources = []
        for item in new_value:
            if isinstance(item, Resource):
                resources.append(item)
                continue

            resource = self.resource_type(
                request=self.request,
                application_args=self.application_args,
            )
            resource.update(item)
            resources.append(resource)

        super()._set_value(resources)

    def _get_data(self):
        return [resource.data for resource in self.value]
