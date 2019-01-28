import json
from typing import Type, Union

from toy.http import Request
from toy.resources import Resource


class Processor:
    content_type = None

    def parse(self, stream):
        raise NotImplementedError('Abstract class')

    def serialize(self, obj):
        raise NotImplementedError('Abstract class')


class ProcessorManager:
    def __init__(self):
        self.processors = {}

    def register(self, processor_class: Type[Processor]):
        if not processor_class.content_type:
            raise ValueError('Invalid processor')

        self.processors[processor_class.content_type] = processor_class()
        return processor_class

    def process(self, request: Request, resource: Resource) -> Resource:
        processor = self.processors[request.content_type]
        data = processor.parse(request.data)
        resource.update(data)
        return resource


processor_manager = ProcessorManager()


@processor_manager.register
class JSONProcessor(Processor):
    content_type = 'application/json'

    def parse(self, stream: Union[str, bytes]) -> dict:
        return json.loads(stream)

    def serialize(self, obj: dict) -> str:
        return json.dumps(obj)


# TODO:
#   - xml
#   - html/form
