from decimal import Decimal
from uuid import uuid4

import pytest

from toy import fields
from toy.exceptions import ValidationError, ValidationException
from toy.fields import Field
from toy.resources import Resource


def test_basic_uuid_field():
    field = fields.UUIDField(name='uuid')

    uuid = uuid4()
    field.value = uuid

    assert field.name == 'uuid'
    assert field.value == uuid


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
    field = fields.ResourceField(name='resource', resource_type=Resource)
    field.value = Resource()

    assert field.validate() == []
    assert field.name == 'resource'
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
    field.value = Resource()

    assert field.validate()[0].message == 'Invalid value type for this field'


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

    field.value = SpecificResource()  # not list
    assert field.validate()[0].message == 'Field must be a list or tuple'

    field.value = [Resource()]
    assert field.validate()[0].message == 'Invalid value type for this field'


def test_fail_resource_list_field_resource_type():
    with pytest.raises(TypeError):
        fields.ResourceListField(name='resource_list', resource_type=object)


def test_fail_invalid_validator():
    with pytest.raises(TypeError):
        Field(name='field', validators=[object()])


def test_field_required_validation():
    field = fields.CharField(name='name', max_length=255, validators=[fields.Required()])

    errors = field.validate()
    assert errors[0].message == 'Required field'


def test_basic_validation_error():
    error = ValidationError('message', 'name', 'value')

    assert error.message == 'message'
    assert error.name == 'name'
    assert error.value == 'value'
    assert repr(error) == "<ValidationError message 'name' 'value'>"


def test_type_validation():
    validation = fields.Type()
    assert validation.allowed_types == ()

    validation = fields.Type([str])
    assert validation.allowed_types == (str,)


def test_length_validation():
    validation = fields.Length(min_length=5, max_length=10)

    assert validation.min_length == 5
    assert validation.max_length == 10


def test_fail_invalid_length_validation():
    with pytest.raises(ValueError):
        fields.Length(min_length=10, max_length=5)


def test_field_length_validation():
    field = fields.CharField(name='name', max_length=10, validators=[fields.Length(min_length=5)])

    field.value = 'X' * 5
    field.validate(raise_exception=True)

    field.value = 'X'
    errors = field.validate()
    assert errors[0].message == 'Invalid min length'

    field.value = 'X' * 15
    errors = field.validate()
    assert errors[0].message == 'Invalid max length'

    field.value = 0
    errors = field.validate()
    assert errors[1].message == 'Value has no length'


def test_range_validation():
    validation = fields.Range(min_value=5, max_value=10)

    assert validation.min_value == 5
    assert validation.max_value == 10


def test_fail_invalid_range_validation():
    with pytest.raises(ValueError):
        fields.Range(min_value=10, max_value=5)


def test_field_range_validation():
    field = fields.IntegerField(name='int', min_value=5, max_value=10)

    field.value = 5
    field.validate(raise_exception=True)

    field.value = 1
    errors = field.validate()
    assert errors[0].message == 'Invalid min value'

    field.value = 15
    errors = field.validate()
    assert errors[0].message == 'Invalid max value'

    field.value = None
    errors = field.validate()
    assert errors[0].message == 'Invalid value type for this field'


def test_skip_field_validation_lazy_fields():
    field = fields.CharField(name='name', max_length=255, lazy=True, validators=[fields.Required()])
    field.validate(include_lazy=False)
    with pytest.raises(ValidationException):
        field.validate(raise_exception=True)


def test_field_dirtyness():
    field = fields.CharField(name='name', max_length=255)
    assert field.dirty is False

    field.value = 'dirty value'
    assert field.dirty is True

    field.clean()
    assert field.dirty is False

    field.value = 'dirty value'
    assert field.dirty is False

    field.value = 'temp dirty'
    field.value = 'dirty value'
    assert field.dirty is False
