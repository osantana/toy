import pytest

from toy.serializers import JSONSerializer, Serializer, SerializersManager


def test_basic_json_processor():
    processor = JSONSerializer()

    data = processor.load('{"obj": "value"}')
    assert data['obj'] == 'value'

    data = processor.dump(data)
    assert data == '{"obj": "value"}'


def test_serializer_manager_register():
    manager = SerializersManager.get()

    @manager.register
    class MySerializer(Serializer):
        content_type = 'application/octet-stream'

        def load(self, stream):
            return stream

        def dump(self, data: dict):
            return data

    processor = manager['application/octet-stream']
    assert isinstance(processor, MySerializer)


def test_fail_processor_manager_register_no_content_type():
    manager = SerializersManager.get()

    with pytest.raises(ValueError):
        manager.register(Serializer)
