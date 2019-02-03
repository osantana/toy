import json
from typing import Type, Union


# TODO:
#   - xml
#   - html/form


class Serializer:
    content_type = None

    def load(self, stream):
        raise NotImplementedError('Abstract class')  # pragma: nocover

    def dump(self, obj):
        raise NotImplementedError('Abstract class')  # pragma: nocover


class SerializersManager:
    _instance = None

    def __init__(self):
        self._serializers = {}

    def register(self, serializer_class: Type[Serializer]):
        if not serializer_class.content_type:
            raise ValueError('Invalid serializer')

        self._serializers[serializer_class.content_type] = serializer_class()
        return serializer_class

    def __getitem__(self, item):
        return self._serializers[item]

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


serializers = SerializersManager.get()


@serializers.register
class JSONSerializer(Serializer):
    content_type = 'application/json'

    def load(self, stream: Union[str, bytes]) -> dict:
        return json.loads(stream)

    def dump(self, obj: dict) -> str:
        return json.dumps(obj)
