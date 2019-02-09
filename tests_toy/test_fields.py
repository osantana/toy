from decimal import Decimal
from uuid import uuid4

import pytest

from toy import fields
from toy.exceptions import ValidationException
from toy.resources import Resource


def test_basic_uuid_field():
    field = fields.UUIDField(name='uuid')

    uuid = uuid4()
    field.value = uuid

    assert field.name == 'uuid'
    assert field.value == uuid
    assert field.data == str(uuid)


def test_uuid_field_not_defined():
    field = fields.UUIDField(name='uuid')

    assert field.name == 'uuid'
    assert field.value is None
    assert field.data is None


def test_error_invalid_uuid():
    field = fields.UUIDField(name='uuid')

    field.value = 'invalid uuid'
    assert field.validate()[0].message == 'Invalid value type for this field'


def test_basic_char_field():
    field = fields.CharField(name='char', max_length=100)
    field.value = 'value'

    assert field.name == 'char'
    assert field.value == 'value'
    assert field.validate() == []


def test_error_invalid_char_field():
    field = fields.CharField(name='char', max_length=1)
    field.value = 'invalid'

    with pytest.raises(ValidationException):
        field.validate(raise_exception=True)


def test_check_equality_with_char_value():
    field1 = fields.CharField(name='test', max_length=100)
    field1.value = 'value'

    field2 = fields.CharField(name='test', max_length=100)
    field2.value = 'value'

    assert field1 == 'value'
    assert field2 == 'value'
    assert field1 == field2
    assert field1 is not field2


def test_basic_integer_field():
    field = fields.IntegerField(name='int')
    field.value = 7

    assert field.validate() == []
    assert field.name == 'int'
    assert field.value == 7


def test_integer_field_with_range():
    field = fields.IntegerField(name='int', min_value=5, max_value=10)
    field.value = 7

    assert field.validate() == []
    assert field.name == 'int'
    assert field.value == 7


def test_fail_invalid_type_in_integer_field():
    field = fields.IntegerField(name='int', min_value=5, max_value=10)

    field.value = 6.5
    assert field.validate()[0].message == 'Invalid value type for this field'

    field.value = Decimal('6.0')
    assert field.validate()[0].message == 'Invalid value type for this field'


def test_basic_boolean_field():
    field = fields.BooleanField(name='bool')
    field.value = True

    assert field.name == 'bool'
    assert field.value is True


def test_fail_invalid_value_in_boolean_field():
    field = fields.BooleanField(name='bool')

    field.value = ''
    assert field.validate()[0].message == 'Invalid value type for this field'


def test_basic_resource_field():
    class MyResource(Resource):
        fields = [
            fields.CharField(name='name', max_length=255),
        ]

    field = fields.ResourceField(name='resource', resource_type=MyResource)
    field.value = {'name': 'My Name'}

    assert field.validate() == []
    assert field.name == 'resource'
    assert field.resource_type == MyResource
    assert isinstance(field.value, MyResource)
    assert field.value['name'] == 'My Name'
    assert isinstance(field.data, dict)
    assert field.data == {'name': 'My Name'}


def test_empty_resource_field():
    class MyResource(Resource):
        fields = [
            fields.CharField(name='name', max_length=255),
        ]

    field = fields.ResourceField(name='resource', resource_type=MyResource)

    assert field.validate() == []
    assert field.name == 'resource'
    assert field.resource_type == MyResource
    assert field.data is None


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
    field.value = Resource()

    assert field.validate()[0].message == 'Invalid value type for this field'
    assert field.data == {}


def test_basic_resource_list_field():
    field = fields.ResourceListField(name='resource_list', resource_type=Resource)
    field.value = [Resource()]

    assert field.name == 'resource_list'
    assert field.resource_type == Resource
    assert isinstance(field.value[0], Resource)
    assert field.data == [{}]


def test_empty_resource_list_field():
    field = fields.ResourceListField(name='resource_list', resource_type=Resource)

    assert field.name == 'resource_list'
    assert field.resource_type == Resource
    assert field.value == []
    assert field.data == []


def test_fail_invalid_resource_in_resource_list_field_value(application):
    # noinspection PyAbstractClass
    class SpecificResource(Resource):
        pass

    field = fields.ResourceListField(name='resource', resource_type=SpecificResource)

    field.value = SpecificResource()  # not list
    assert field.validate()[0].message == 'Field must be a list or tuple'

    field.value = [Resource()]
    assert field.validate()[0].message == 'Invalid value type for this field'


def test_fail_resource_list_field_resource_type():
    with pytest.raises(TypeError):
        fields.ResourceListField(name='resource_list', resource_type=object)
