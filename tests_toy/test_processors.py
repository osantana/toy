import pytest

from toy.processors import JSONProcessor, Processor, ProcessorManager, processor_manager


def test_basic_json_processor():
    processor = JSONProcessor()

    data = processor.parse('{"obj": "value"}')
    assert data['obj'] == 'value'

    data = processor.serialize(data)
    assert data == '{"obj": "value"}'


def test_processor_manager_register():
    manager = ProcessorManager()

    @manager.register
    class MyProcessor(Processor):
        content_type = 'application/octet-stream'

        def parse(self, stream):
            return stream

        def serialize(self, data: dict):
            return data

    processor = manager.processors['application/octet-stream']
    assert isinstance(processor, MyProcessor)


def test_fail_processor_manager_register_no_content_type():
    manager = ProcessorManager()

    with pytest.raises(ValueError):
        manager.register(Processor)


def test_global_processor(post_request, resource):
    resource = processor_manager.process(post_request, resource)

    assert resource['name'] == 'My Name'
    assert resource['description'] == 'My Description'
