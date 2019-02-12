import pytest

from toy import fields, validators
from toy.exceptions import ValidationError, ValidationException
from toy.fields import Field


def test_type_validation():
    validation = validators.Type()
    assert validation.allowed_types == ()

    validation = validators.Type([str])
    assert validation.allowed_types == (str,)


def test_length_validation():
    validation = validators.Length(min_length=5, max_length=10)

    assert validation.min_length == 5
    assert validation.max_length == 10


def test_fail_invalid_length_validation():
    with pytest.raises(ValueError):
        validators.Length(min_length=10, max_length=5)

    with pytest.raises(ValueError):
        validators.Length(min_length=-1, max_length=5)

    with pytest.raises(ValueError):
        validators.Length(min_length=-5, max_length=-10)

    with pytest.raises(ValueError):
        validators.Length(min_length='5', max_length=10)

    with pytest.raises(ValueError):
        validators.Length(min_length=5, max_length='10')


def test_field_length_validation():
    field = fields.CharField(name='name', max_length=10, validators=[validators.Length(min_length=5)])

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
    validation = validators.Range(min_value=5, max_value=10)

    assert validation.min_value == 5
    assert validation.max_value == 10


def test_fail_invalid_range_validation():
    with pytest.raises(ValueError):
        validators.Range(min_value=10, max_value=5)


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
    field = fields.CharField(name='name', max_length=255, lazy=True, validators=[validators.Required()])
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


def test_fail_invalid_validator():
    with pytest.raises(TypeError):
        Field(name='field', validators=[object()])


def test_field_required_validation():
    field = fields.CharField(name='name', max_length=255, validators=[validators.Required()])

    errors = field.validate()
    assert errors[0].message == 'Required field'


def test_basic_validation_error():
    error = ValidationError('message', 'name', 'value')

    assert error.message == 'message'
    assert error.name == 'name'
    assert error.value == 'value'
    assert repr(error) == "<ValidationError message 'name' 'value'>"
