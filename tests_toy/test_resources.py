import pytest

from toy import fields
from toy.resources import Resource, Processor


def test_basic_resource():
    # noinspection PyAbstractClass
    class MyResource(Resource):
        fields = [
            fields.CharField(name='name', max_length=255),
            fields.CharField(name='description', max_length=255)
        ]

    resource = MyResource()

    assert isinstance(resource, MyResource)
    assert 'name' in resource
    assert 'description' in resource


def test_fail_abstract_resource():
    # noinspection PyAbstractClass
    class MyResource(Resource):
        pass

    resource = MyResource()

    with pytest.raises(NotImplementedError):
        resource.get()


def test_basic_resource_update(resource):
    resource.get()
    resource.update({
        'name': 'My New Name',
    })

    assert resource['name'] == 'My New Name'


def test_basic_resource_data(resource):
    resource.get()

    assert resource.data == {
        'name': 'My Name',
        'description': 'My Description',
    }


def test_fail_set_invalid_field(resource):
    with pytest.raises(ValueError):
        resource['invalid'] = 'value'


def test_processor_get_data(post_request):
    processor = Processor(post_request)
    data = processor.get_data()

    assert data['name'] == 'My Name'
    assert data['description'] == 'My Description'


def test_processor_get_response(post_request, json_data):
    processor = Processor(post_request)
    response = processor.get_response(processor.get_data())

    assert response.status == 200
    assert response.data == json_data
