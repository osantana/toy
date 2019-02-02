from decimal import Decimal
from uuid import uuid4

import pytest

from toy import fields
from toy.exceptions import ValidationError
from toy.resources import Resource


def test_basic_uuid_field():
    field = fields.UUIDField(name='uuid')

    uuid = uuid4()
    field.value = uuid

    assert field.name == 'uuid'
    assert field.value == uuid


def test_error_invalid_uuid():
    field = fields.UUIDField(name='uuid')

    with pytest.raises(ValueError):
        field.value = 'invalid uuid'


def test_basic_char_field():
    field = fields.CharField(name='char', max_length=100)
    field.value = 'value'

    assert field.name == 'char'
    assert field.max_length == 100
    assert field.value == 'value'


def test_error_invalid_char_field():
    field = fields.CharField(name='char', max_length=1)

    with pytest.raises(ValueError):
        field.value = 'invalid'


def test_check_equality_with_char_value():
    field = fields.CharField(name='test', max_length=100)
    field.value = 'value'

    assert field == 'value'


def test_basic_integer_field():
    field = fields.IntegerField(name='int')
    field.value = 7

    assert field.name == 'int'
    assert field.min_value is None
    assert field.max_value is None
    assert field.value == 7


def test_integer_field_with_range():
    field = fields.IntegerField(name='int', min_value=5, max_value=10)
    field.value = 7

    assert field.name == 'int'
    assert field.min_value == 5
    assert field.max_value == 10
    assert field.value == 7


def test_fail_integer_field_invalid_value_range():
    with pytest.raises(ValueError):
        fields.IntegerField(name='int', min_value=10, max_value=5)


def test_fail_invalid_value_in_integer_field():
    field = fields.IntegerField(name='int', min_value=5, max_value=10)

    with pytest.raises(ValueError):
        field.value = 100

    with pytest.raises(ValueError):
        field.value = 1


def test_fail_invalid_type_in_integer_field():
    field = fields.IntegerField(name='int', min_value=5, max_value=10)

    with pytest.raises(TypeError):
        field.value = 6.5

    with pytest.raises(TypeError):
        field.value = Decimal('6.0')


def test_basic_boolean_field():
    field = fields.BooleanField(name='bool')
    field.value = True

    assert field.name == 'bool'
    assert field.value is True


def test_fail_invalid_value_in_boolean_field():
    field = fields.BooleanField(name='bool')

    with pytest.raises(ValueError):
        field.value = None


def test_basic_resource_field():
    field = fields.ResourceField(name='resource', resource_type=Resource)
    field.value = Resource()

    assert field.name == 'resource'
    assert field.resource_type == Resource
    assert isinstance(field.value, Resource)


def test_fail_invalid_resource_type_in_resource_field():
    class InvalidResource:
        pass

    with pytest.raises(TypeError):
        fields.ResourceField(name='resource', resource_type=InvalidResource)


def test_fail_invalid_resource_in_resource_field_value(application):
    # noinspection PyAbstractClass
    class SpecificResource(Resource):
        pass

    field = fields.ResourceField(name='resource', resource_type=SpecificResource)

    with pytest.raises(TypeError):
        field.value = Resource()


def test_basic_resource_list_field():
    field = fields.ResourceListField(name='resource_list', resource_type=Resource)
    field.value = [Resource()]

    assert field.name == 'resource_list'
    assert field.resource_type == Resource
    assert isinstance(field.value[0], Resource)


def test_fail_invalid_resource_in_resource_list_field_value(application):
    # noinspection PyAbstractClass
    class SpecificResource(Resource):
        pass

    field = fields.ResourceListField(name='resource', resource_type=SpecificResource)

    with pytest.raises(TypeError):
        field.value = SpecificResource()  # not list

    with pytest.raises(TypeError):
        field.value = [Resource()]


def test_field_validation():
    field = fields.CharField(name='name', max_length=255, validators=[fields.Required()])

    with pytest.raises(ValidationError):
        field.validate()


def test_skip_field_validation_lazy_fields():
    field = fields.CharField(name='name', max_length=255, lazy=True, validators=[fields.Required()])
    field.validate(include_lazy=False)
    with pytest.raises(ValidationError):
        field.validate()


def test_field_dirtyness():
    field = fields.CharField(name='name', max_length=255)
    assert field.dirty is False

    field.value = 'dirty value'
    assert field.dirty is True

    field.clean()
    assert field.dirty is False
