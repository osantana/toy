import pytest

from toy import fields
from toy.resources import Resource


def test_basic_resource():
    class MyResource(Resource):
        fields = [
            fields.CharField(name='name', max_length=255),
            fields.CharField(name='description', max_length=255)
        ]

        def get(self, **kwargs):
            pass

    resource = MyResource(arg='value')

    assert isinstance(resource, MyResource)
    assert 'name' in resource
    assert 'description' in resource
    assert resource.arguments == {'arg': 'value'}


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
