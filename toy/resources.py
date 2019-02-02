from typing import Type

from .http import Response
from .serializers import serializers


class Resource:
    fields = []

    def __init__(self, **arguments):
        self.arguments = arguments
        self._fields = {}

        for field in self.fields:
            self._fields[field.name] = field

    def __setitem__(self, key, value):
        if key not in self._fields:
            raise ValueError('Invalid field')

        self._fields[key].value = value

    def __getitem__(self, item):
        return self._fields[item].value

    def __contains__(self, item):
        return item in self._fields

    def update(self, data):
        for key, value in data.items():
            self[key] = value

    def get(self, **kwargs):
        raise NotImplementedError('Abstract class')

    def create(self, **kwargs):
        raise NotImplementedError('Abstract class')

    @property
    def data(self):
        result = {}
        for key, field in self._fields.items():
            result[key] = field.value
        return result


class RequestProcessor:
    def __init__(self, request, serializers_manager=None):
        self.request = request

        if serializers_manager is None:
            serializers_manager = serializers
        self.serializers = serializers_manager

    def process_payload(self, resource_class: Type[Resource]) -> Resource:
        resource = resource_class(
            args=self.request.args,
            query_string=self.request.query_string,
        )

        serializer = self.serializers[self.request.content_type]

        resource_data = serializer.load(self.request.data)
        resource.update(resource_data)

        return resource

    def process_resource(self, resource: Resource) -> Response:
        # TODO
        pass
