import json
import pytest

from ckantoolkit import Invalid

from ckanext.validation.validators import (
    resource_schema_validator,
    validation_options_validator,
)


class TestResourceSchemaValidator(object):
    def test_resource_schema_none(self):

        schema = ""

        assert resource_schema_validator(schema, {}) is None

    def test_resource_schema_invalid_json_string(self):

        schema = "{a,b}"

        with pytest.raises(Invalid):
            resource_schema_validator(schema, {})

    def test_resource_schema_invalid_schema_string(self):

        schema = '{"a": 1}'

        with pytest.raises(Invalid):
            resource_schema_validator(schema, {})

    def test_resource_schema_valid_json_not_a_dict_string(self):

        schema = "[a,2]"

        with pytest.raises(Invalid):
            resource_schema_validator(schema, {})

    def test_resource_schema_valid_json_empty_string(self):

        schema = '""'

        with pytest.raises(Invalid):
            resource_schema_validator(schema, {})

    def test_resource_schema_invalid_schema_object(self):

        schema = {"a": 1}

        with pytest.raises(Invalid) as e:
            resource_schema_validator(schema, {})

        assert e.value.error.startswith(
            "Invalid Table Schema: "
            + "Descriptor validation error: 'fields' is a required property"
        )

    def test_resource_schema_valid_schema_object(self):

        schema = {"fields": [{"name": "longitude"}]}

        value = resource_schema_validator(schema, {})

        assert value == json.dumps(schema)

    def test_resource_schema_valid_schema_string(self):

        schema = '{"fields": [{"name": "longitude"}]}'

        value = resource_schema_validator(schema, {})

        assert value == schema

    def test_resource_schema_valid_schema_url(self):

        schema = "https://example.com/schema.json"

        value = resource_schema_validator(schema, {})

        assert value == schema

    def test_resource_schema_invalid_wrong_url(self):

        schema = "/some/wrong/url/schema.json"

        with pytest.raises(Invalid):
            resource_schema_validator(schema, {})


class TestValidationOptionsValidator(object):
    """
    Note: At the point this validator is run the value should already
        be a valid JSON string (ie `scheming_valid_json_object` has been
        run)
    """

    def test_no_default_validation_options(self):

        value = '{"limit_rows":3}'

        assert validation_options_validator(value, {}) == value

    @pytest.mark.ckan_config(
        "ckanext.validation.default_validation_options", '{"encoding":"utf-8"}'
    )
    def test_default_validation_options(self):

        value = '{"limit_rows": 3}'

        assert (
            validation_options_validator(value, {})
            == '{"encoding": "utf-8", "limit_rows": 3}'
        )

    @pytest.mark.ckan_config(
        "ckanext.validation.default_validation_options",
        '{"encoding":"utf-8", "limit_rows":2}',
    )
    def test_default_validation_optionsi_does_not_override(self):

        value = '{"limit_rows": 3}'

        assert (
            validation_options_validator(value, {})
            == '{"encoding": "utf-8", "limit_rows": 3}'
        )

    def test_empty_value_is_passed_through(self):

        assert validation_options_validator('', {}) == ''

    def test_unknown_option_is_rejected(self):
        """A Table Schema descriptor put here instead of in `schema` used to
        reach Frictionless and fail there, without ever opening the file."""

        value = '{"fields": [{"name": "a", "type": "number"}]}'

        with pytest.raises(Invalid) as e:
            validation_options_validator(value, {})

        assert "Unknown validation option: fields" in str(e.value)

    def test_unknown_options_are_all_listed(self):

        value = '{"headers": 3, "delimiter": ";", "dialect": {}}'

        with pytest.raises(Invalid) as e:
            validation_options_validator(value, {})

        assert "Unknown validation options: delimiter, headers" in str(e.value)

    @pytest.mark.ckan_config(
        "ckanext.validation.default_validation_options", '{"headers":3}'
    )
    def test_unknown_option_from_config_is_rejected(self):

        with pytest.raises(Invalid):
            validation_options_validator('{"limit_rows": 3}', {})
