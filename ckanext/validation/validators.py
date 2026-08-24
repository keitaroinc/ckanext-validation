# encoding: utf-8
import json

import tableschema

from ckantoolkit import Invalid, config


# Options the validation job is allowed to forward to
# `frictionless.validate()`. `source`, `format` and `schema` are passed by the
# job itself, so supplying them here raises a "multiple values for keyword
# argument" TypeError. Anything else is either meaningless to `validate()` or,
# worse, quietly accepted by `Resource` with an entirely different meaning:
# `fields`, for instance, is a field *count*, not a Table Schema, so a schema
# descriptor put here fails without ever opening the file.
VALIDATION_OPTIONS = frozenset([
    # Checklist
    u'checklist',
    u'checks',
    u'pick_errors',
    u'skip_errors',
    # Limits
    u'limit_errors',
    u'limit_rows',
    # Resource options `validate()` forwards
    u'compression',
    u'detector',
    u'dialect',
    u'encoding',
    u'innerpath',
])


# Input validators

def resource_schema_validator(value, context):

    if not value:
        return

    msg = None

    if isinstance(value, dict):
        descriptor = value
    else:
        value = str(value)

        if value.lower().startswith('http'):
            return value

        try:
            descriptor = json.loads(str(value))
            if not isinstance(descriptor, dict):
                msg = u'Invalid Table Schema descriptor: {}'.format(value)
                raise Invalid(msg)

        except ValueError as e:
            msg = u'JSON error in Table Schema descriptor: {}'.format(e)
            raise Invalid(msg)

    try:
        tableschema.validate(descriptor)
    except tableschema.exceptions.ValidationError as e:
        errors = []
        for error in e.errors:
            errors.append(str(error))
        msg = u'Invalid Table Schema: {}'.format(u', '.join(errors))

    if msg:
        raise Invalid(msg)

    return json.dumps(descriptor)


def validation_options_validator(value, context):
    '''Add default validation options if not already present, and reject
    options that the validation job can not pass on to Frictionless.

    At this point the value should already be a valid JSON string (ie
    `scheming_valid_json_object` has been run).
    '''

    if not value:
        return value

    default_options = config.get(
        'ckanext.validation.default_validation_options')

    if default_options:
        default_options = json.loads(default_options)

        provided_options = json.loads(value)

        default_options.update(provided_options)

        value = json.dumps(default_options, indent=None, sort_keys=True)

    options = value if isinstance(value, dict) else json.loads(value)

    unknown = sorted(set(options) - VALIDATION_OPTIONS)
    if unknown:
        raise Invalid(
            u'Unknown validation option{plural}: {unknown}. '
            u'Supported options are: {supported}'.format(
                plural=u's' if len(unknown) > 1 else u'',
                unknown=u', '.join(unknown),
                supported=u', '.join(sorted(VALIDATION_OPTIONS))))

    return value
