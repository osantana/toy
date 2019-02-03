import pytest

from toy import fields
from toy.exceptions import ValidationException
from toy.resources import Processor, Resource


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


def test_validate_resource_all_fields(basic_resource_class):
    resource = basic_resource_class(
        name='Name',
        description='Description',
        slug='slug'
    )
    resource.validate()


def test_validate_resource_only_required_fields(basic_resource_class):
    resource = basic_resource_class(
        name='Name',
        slug='slug'
    )
    resource.validate()


def test_validate_resource_exclude_lazy(basic_resource_class):
    resource = basic_resource_class(
        name='Name',
        description='Description',
    )
    resource.validate(include_lazy=False)


def test_fail_validate_resource_missing_field(basic_resource_class):
    resource = basic_resource_class(
        name='Name',
        description='Description',
    )

    with pytest.raises(ValidationException) as exc_info:
        resource.validate(raise_exception=True)

    exc = exc_info.value
    assert len(exc.errors) == 1
    assert exc.errors['slug'][0].message == 'Required field'


def test_fail_validate_resource_unknown_field(basic_resource_class):
    resource = basic_resource_class(
        name='Name',
        description='Description',
        slug='slug',
        unknown='error'
    )
    with pytest.raises(ValidationException) as exc_info:
        resource.validate(raise_exception=True)

    exc = exc_info.value
    assert len(exc.errors) == 1
    assert exc.errors['unknown'][0].message == 'Extra field data'


def test_validate_resource_unknown_extra_field(basic_resource_class):
    basic_resource_class.ignore_extra_data = True
    resource = basic_resource_class(
        name='Name',
        description='Description',
        slug='slug',
        unknown='error'
    )
    assert resource.validate() == {}
