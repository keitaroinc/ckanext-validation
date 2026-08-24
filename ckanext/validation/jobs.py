# encoding: utf-8

import logging
import datetime
import json
import re

import requests
from sqlalchemy.orm.exc import NoResultFound
from frictionless import validate, system, Report, Schema, Dialect, Check

from ckan.common import config
from ckan.model import Session
import ckan.lib.uploader as uploader

import ckantoolkit as t

from ckanext.validation.model import Validation
from ckanext.validation.utils import get_update_mode_from_config


log = logging.getLogger(__name__)


def run_validation_job(resource):

    log.debug('Validating resource %s', resource['id'])

    try:
        validation = Session.query(Validation).filter(
            Validation.resource_id == resource['id']).one()
    except NoResultFound:
        validation = None

    if not validation:
        validation = Validation(resource_id=resource['id'])

    validation.status = 'running'
    Session.add(validation)
    Session.commit()

    options = t.config.get(
        'ckanext.validation.default_validation_options')
    if options:
        options = json.loads(options)
    else:
        options = {}

    resource_options = resource.get('validation_options')
    if resource_options and isinstance(resource_options, str):
        resource_options = json.loads(resource_options)
    if resource_options:
        options.update(resource_options)

    dataset = t.get_action('package_show')(
        {'ignore_auth': True}, {'id': resource['package_id']})

    source = None
    # Token minted for this run only, revoked once the validation finishes
    temp_api_token = None
    if resource.get('url_type') == 'upload':
        upload = uploader.get_resource_uploader(resource)
        if isinstance(upload, uploader.ResourceUpload):
            source = upload.get_path(resource['id'])
        else:
            # Upload is not the default implementation (ie it's a cloud storage
            # implementation)
            pass_auth_header = t.asbool(
                t.config.get('ckanext.validation.pass_auth_header', True))
            if dataset['private'] and pass_auth_header:
                auth_header_value = t.config.get(
                    'ckanext.validation.pass_auth_header_value')
                if not auth_header_value:
                    auth_header_value = temp_api_token = \
                        _create_site_user_api_token()

                auth_header_name = _get_api_token_header_name()
                s = AuthHeaderSession(auth_header_name)
                s.headers.update({auth_header_name: auth_header_value})

                options['http_session'] = s

    if not source:
        source = _resolve_source_url(resource['url'])

    schema = resource.get('schema')
    if schema:
        if isinstance(schema, str):
            if schema.startswith('http'):
                r = requests.get(schema)
                schema = r.json()
            schema = json.loads(schema)

    _format = resource['format'].lower()
    try:
        report = _validate_table(
            source, _format=_format, schema=schema, **options)
    finally:
        if temp_api_token:
            _revoke_api_token(temp_api_token)

    # Hide uploaded files
    if type(report) == Report:
        report = report.to_dict()

    if 'tasks' in report:
        for table in report['tasks']:
            if table['place'].startswith('/') or table['place'] == source:
                table['place'] = resource['url']

    # Frictionless warnings are truncation notices ("reached row limit: 100"),
    # not failures, so they don't decide the status. They can still quote the
    # local path of an uploaded file, so hide it.
    for index, warning in enumerate(report.get('warnings') or []):
        report['warnings'][index] = re.sub(r'Table ".*"', 'Table', warning)

    validation.report = json.dumps(report)

    if 'valid' in report:
        validation.status = 'success' if report['valid'] else 'failure'
    else:
        # No `valid` key means the run did not get far enough to reach a
        # verdict, so the status is always an error rather than a result.
        validation.status = 'error'
        if report.get('errors'):
            validation.error = {
                'message': [str(err) for err in report['errors']]}
        else:
            validation.error = {'message': ['Errors validating the data']}
    validation.finished = datetime.datetime.utcnow()

    Session.add(validation)
    Session.commit()

    # Store result status in resource
    data_dict = {
        'id': resource['id'],
        'validation_status': validation.status,
        'validation_timestamp': validation.finished.isoformat(),
    }

    if get_update_mode_from_config() == 'sync':
        data_dict['_skip_next_validation'] = True,

    patch_context = {
        'ignore_auth': True,
        'user': t.get_action('get_site_user')({'ignore_auth': True})['name'],
        '_validation_performed': True
    }
    t.get_action('resource_patch')(patch_context, data_dict)




def _resolve_source_url(url):
    """Return the URL the validation worker should download the resource from.

    Resource URLs are built from ``ckan.site_url``, which is not necessarily
    reachable from the worker (eg a local development instance, or a container
    with no route back in through the public load balancer). Those deployments
    can set ``ckanext.validation.internal_site_url`` to a base URL that *is*
    reachable, eg::

        ckanext.validation.internal_site_url = http://localhost:5000

    and the site URL prefix is swapped for it. When the option is not set the
    resource URL is used unchanged.
    """
    internal_site_url = (
        config.get('ckanext.validation.internal_site_url', '') or '').rstrip('/')
    site_url = (config.get('ckan.site_url', '') or '').rstrip('/')

    if not internal_site_url or not site_url or not url.startswith(site_url):
        return url

    resolved = internal_site_url + url[len(site_url):]
    log.debug('Resolved resource URL %s to %s for validation', url, resolved)
    return resolved


def _validate_table(source, _format='csv', schema=None, **options):

    # This option is needed to allow Frictionless Framework to validate absolute paths
    frictionless_context = { 'trusted': True }
    http_session = options.pop('http_session', None) or requests.Session()
    use_proxy = 'ckan.download_proxy' in t.config

    if use_proxy:
        proxy = t.config.get('ckan.download_proxy')
        log.debug('Download resource for validation via proxy: %s', proxy)
        http_session.proxies.update({'http': proxy, 'https': proxy})

    frictionless_context['http_session'] = http_session
    resource_schema = Schema.from_descriptor(schema) if schema else None

    # Load the Resource Dialect as described in https://framework.frictionlessdata.io/docs/framework/dialect.html
    if 'dialect' in options:
        dialect = Dialect.from_descriptor(options['dialect'])
        options['dialect'] = dialect

    # Load the list of checks and its parameters declaratively as in https://framework.frictionlessdata.io/docs/checks/table.html
    if 'checks' in options:
        checklist = [Check.from_descriptor(c) for c in options['checks']]
        options['checks'] = checklist

    with system.use_context(**frictionless_context):
        report = validate(source, format=_format, schema=resource_schema, **options)
        log.debug('Validating source: %s', source)

    return report


class AuthHeaderSession(requests.Session):
    """Session that drops the CKAN auth header when redirected to another host.

    Cloud storage backends answer the CKAN download URL with a redirect to a
    signed URL on the storage host, so the credential must not travel with it.
    ``requests`` already does this for ``Authorization``, but CKAN can be
    configured to read tokens from a different header via
    ``apitoken_header_name``, which it knows nothing about.
    """

    def __init__(self, auth_header_name):
        super(AuthHeaderSession, self).__init__()
        self.auth_header_name = auth_header_name

    def rebuild_auth(self, prepared_request, response):
        super(AuthHeaderSession, self).rebuild_auth(prepared_request, response)

        if self.auth_header_name.lower() == 'authorization':
            # Already handled by requests itself
            return

        if self.should_strip_auth(response.request.url, prepared_request.url):
            prepared_request.headers.pop(self.auth_header_name, None)


def _get_api_token_header_name():
    """Name of the header CKAN reads API tokens from (``Authorization``)."""
    return t.config.get('apitoken_header_name', 'Authorization')


def _create_site_user_api_token():
    """Create an API token for the site user and return the encoded token.

    Needed to download private resources that are served through CKAN by a
    cloud storage backend. The legacy ``user.apikey`` this used to send is no
    longer an authentication credential -- CKAN resolves the token header with
    ``ckan.lib.api_token.get_user_from_token``, which only accepts real API
    tokens -- so sending the API key silently produced a `Not Authorized`
    error.

    The token is revoked by :func:`_revoke_api_token` as soon as the
    validation run finishes, so no long-lived credential is left behind.
    """
    site_user = t.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'ignore_auth': True, 'user': site_user['name']}

    token = t.get_action('api_token_create')(context, {
        'user': site_user['name'],
        'name': 'ckanext-validation',
    })

    return token['token']


def _revoke_api_token(token):
    """Revoke a token created by :func:`_create_site_user_api_token`."""
    site_user = t.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'ignore_auth': True, 'user': site_user['name']}

    try:
        t.get_action('api_token_revoke')(context, {'token': token})
    except Exception:
        # Never let cleanup mask the outcome of the validation itself
        log.exception('Could not revoke the API token used for validation')
