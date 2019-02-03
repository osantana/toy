from typing import Optional

from staty import HTTPStatus, Ok

from toy.exceptions import ValidationException, ValidationError
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
            if field.name in self._fields:
                raise TypeError('Duplicated field name')

            self._fields[field.name] = field

        self._extra_data = {}
        self.update(data)

    def __setitem__(self, key, value):
        if key not in self._fields:
            self._extra_data[key] = value
            return

        self._fields[key].value = value

    def __getitem__(self, item):
        return self._fields[item].value

    def __contains__(self, item):
        return item in self._fields

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
            result[key] = field.value
        return result

    @classmethod
    def get(cls, request=None, application_args=None):
        resource = cls.do_get(request, application_args)
        resource.validate()
        return resource

    def create(self):
        self.validate(include_lazy=False)
        self.do_create()
        self.validate()

    def replace(self):
        self.validate()
        self.do_replace()

    def change(self, **kwargs):
        self.validate()
        self.do_change(**kwargs)

    @classmethod
    def do_get(cls, request=None, application_args=None):  # maps to get
        raise NotImplementedError('Abstract class')

    def do_create(self):  # maps to post
        raise NotImplementedError('Abstract class')

    def do_replace(self):  # maps to put
        raise NotImplementedError('Abstract class')

    def do_change(self, **kwargs):  # maps to patch
        raise NotImplementedError('Abstract class')


class Processor:
    def __init__(self, request: Request, serializers_manager=None):
        self.request = request

        if serializers_manager is None:
            serializers_manager = serializers
        self.serializers = serializers_manager

    def get_data(self) -> dict:
        serializer = self.serializers[self.request.content_type]
        return serializer.load(self.request.data)

    def get_response(self, data: dict, status: Optional[HTTPStatus] = None, headers=None, **kwargs) -> Response:
        if status is None:
            status = Ok()

        content_type = self.request.accept[0].media_type
        serializer = self.serializers[content_type]
        data = serializer.dump(data)

        response = Response(
            data=data,
            status=status,
            content_type=content_type,
            headers=headers,
            **kwargs,
        )
        return response
