from typing import Optional

from staty import HTTPStatus, Ok

from .exceptions import UnsupportedMediaTypeException, ValidationError, ValidationException
from .http import Request, Response
from .serializers import serializers


class Resource:
    fields = []
    ignore_extra_data = False

    def __init__(self, request: Optional[Request] = None, application_args=None, **data):
        self.request = request

        if application_args is None:
            application_args = {}
        self.application_args = application_args

        self._fields = {}
        for field in self.fields:
            field_copy = field.copy()
            if field_copy.name in self._fields:
                raise TypeError('Duplicated field name')

            self._fields[field_copy.name] = field_copy
            field_copy.request = request
            field_copy.application_args = application_args

        self._extra_data = {}
        self.update(data)

    def __setitem__(self, key, value):
        if key not in self._fields:
            self._extra_data[key] = value
            return

        self._fields[key].value = value

    def __getitem__(self, item):
        return self._fields[item].value

    def keys(self, include_lazy=True):
        return set(f.name for f in self._fields.values() if include_lazy or not f.lazy)

    def update(self, data):
        for key, value in data.items():
            self[key] = value

    def validate(self, include_lazy=True, raise_exception=False):
        errors = {}
        for field in self._fields.values():
            error = field.validate(include_lazy=include_lazy)
            if not error:
                continue
            errors[field.name] = error

        if self.ignore_extra_data:
            return errors

        if not self.ignore_extra_data and self._extra_data:
            for key, value in self._extra_data.items():
                errors[key] = [ValidationError('Extra field data', name=key, value=value)]

        if raise_exception and errors:
            raise ValidationException('Validation Error', errors=errors)

        return errors

    @property
    def data(self):
        result = {}
        for key, field in self._fields.items():
            result[key] = field.data
        return result

    @classmethod
    def get(cls, request=None, application_args=None) -> 'Resource':
        resource = cls.do_get(request, application_args)
        resource.validate()
        return resource

    def create(self, parent_resource=None) -> 'Resource':
        self.validate(include_lazy=False, raise_exception=True)
        resource = self.do_create(parent_resource)
        self.validate(raise_exception=True)
        return resource or self

    def replace(self) -> 'Resource':
        self.validate()
        resource = self.do_replace()
        return resource or self

    # TODO: kwargs could be used to implement JSON-Patch in the future
    def change(self, **kwargs) -> 'Resource':
        self.validate()
        resource = self.do_change(**kwargs)
        return resource or self

    def remove(self):
        resource = self.do_remove()
        return resource

    @classmethod
    def do_get(cls, request=None, application_args=None) -> Optional['Resource']:  # maps to get
        pass  # pragma: nocover

    def do_create(self, parent_resource=None) -> Optional['Resource']:  # maps to post
        pass  # pragma: nocover

    def do_replace(self) -> Optional['Resource']:  # maps to put
        pass  # pragma: nocover

    def do_change(self, **kwargs) -> Optional['Resource']:  # maps to patch
        pass  # pragma: nocover

    def do_remove(self) -> Optional['Resource']:
        pass  # pragma: nocover


class Processor:
    def __init__(self, request: Request, serializers_manager=None):
        self.request = request

        if serializers_manager is None:
            serializers_manager = serializers
        self.serializers = serializers_manager

    def get_data(self) -> dict:
        serializer = self.serializers[self.request.content_type]
        return serializer.load(self.request.data, self.request.charset)

    def get_response(self, data: dict, status: Optional[HTTPStatus] = None, headers=None, **kwargs) -> Response:
        if status is None:
            status = Ok()

        content_type = self.request.accept[0].media_type
        try:
            serializer = self.serializers[content_type]
        except KeyError:
            raise UnsupportedMediaTypeException(content_type)

        data = serializer.dump(data)

        response = Response(
            data=data,
            status=status,
            content_type=content_type,
            headers=headers,
            **kwargs,
        )
        return response
