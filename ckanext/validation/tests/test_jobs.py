import pytest
from unittest import mock
import json
import io

import ckantoolkit

import requests

from ckan.lib import api_token
from ckan.lib.uploader import ResourceUpload
from ckan.model import ApiToken
from ckan.tests.helpers import call_action
from ckan.tests import factories

from ckanext.validation.model import create_tables, tables_exist, Validation
from ckanext.validation.jobs import (
    run_validation_job,
    uploader,
    Session,
    AuthHeaderSession,
    _resolve_source_url,
)
from ckanext.validation.tests.helpers import (
    VALID_REPORT,
    INVALID_REPORT,
    ERROR_REPORT,
    VALID_REPORT_LOCAL_FILE,
    MockFieldStorage,
    get_mock_file,
)


class MockUploader(ResourceUpload):
    def get_path(self, resource_id):
        return "/tmp/example/{}".format(resource_id)


def mock_get_resource_uploader(data_dict):
    return MockUploader(data_dict)


@pytest.mark.usefixtures("clean_db", "validation_setup")
class TestValidationJob(object):

    @pytest.mark.ckan_config("ckanext.validation.run_on_create_async", False)
    @mock.patch("ckanext.validation.jobs.validate", return_value=VALID_REPORT)
    @mock.patch.object(Session, "commit")
    @mock.patch.object(ckantoolkit, "get_action")
    def test_job_run_no_schema(self, mock_get_action, mock_commit, mock_validate):

        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org["id"])

        resource = {
            "id": "test",
            "url": "http://example.com/file.csv",
            "format": "csv",
            "package_id": dataset["id"],
        }

        run_validation_job(resource)

        assert mock_validate.call_args[0][0] == "http://example.com/file.csv"
        assert mock_validate.call_args[1]["format"] == "csv"
        assert mock_validate.call_args[1]["schema"] is None

    @mock.patch("ckanext.validation.jobs.validate", return_value=VALID_REPORT)
    @mock.patch.object(Session, "commit")
    @mock.patch.object(ckantoolkit, "get_action")
    def test_job_run_schema(self, mock_get_action, mock_commit, mock_validate):

        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org["id"])

        schema = {
            "fields": [
                {"name": "id", "type": "integer"},
                {"name": "description", "type": "string"},
            ]
        }
        resource = {
            "id": "test",
            "url": "http://example.com/file.csv",
            "format": "csv",
            "schema": json.dumps(schema),
            "package_id": dataset["id"],
        }

        run_validation_job(resource)

        assert mock_validate.call_args[0][0] == "http://example.com/file.csv"
        assert mock_validate.call_args[1]["format"] == "csv"
        assert mock_validate.call_args[1]["schema"].to_dict() == schema

    @mock.patch("ckanext.validation.jobs.validate", return_value=VALID_REPORT)
    @mock.patch.object(
        uploader, "get_resource_uploader", return_value=mock_get_resource_uploader({})
    )
    @mock.patch.object(Session, "commit")
    @mock.patch.object(ckantoolkit, "get_action")
    def test_job_run_uploaded_file(
        self, mock_get_action, mock_commit, mock_uploader, mock_validate
    ):

        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org["id"])

        resource = {
            "id": "test",
            "url": "__upload",
            "url_type": "upload",
            "format": "csv",
            "package_id": dataset["id"],
        }

        run_validation_job(resource)

        assert mock_validate.call_args[0][0] == "/tmp/example/{}".format(resource["id"])
        assert mock_validate.call_args[1]["format"] == "csv"
        assert mock_validate.call_args[1]["schema"] is None

    @mock.patch("ckanext.validation.jobs.validate", return_value=VALID_REPORT)
    def test_job_run_valid_stores_validation_object(self, mock_validate):

        resource = factories.Resource(url="http://example.com/file.csv", format="csv")

        run_validation_job(resource)

        validation = (
            Session.query(Validation)
            .filter(Validation.resource_id == resource["id"])
            .one()
        )

        assert validation.status == "success"
        assert json.loads(validation.report) == VALID_REPORT
        assert validation.finished

    @mock.patch("ckanext.validation.jobs.validate", return_value=INVALID_REPORT)
    def test_job_run_invalid_stores_validation_object(self, mock_validate):

        resource = factories.Resource(url="http://example.com/file.csv", format="csv")

        run_validation_job(resource)

        validation = (
            Session.query(Validation)
            .filter(Validation.resource_id == resource["id"])
            .one()
        )

        assert validation.status == "failure"
        assert json.loads(validation.report) == INVALID_REPORT
        assert validation.finished

    @mock.patch("ckanext.validation.jobs.validate", return_value=ERROR_REPORT)
    def test_job_run_error_stores_validation_object(self, mock_validate):

        resource = factories.Resource(url="http://example.com/file.csv", format="csv")

        run_validation_job(resource)

        validation = (
            Session.query(Validation)
            .filter(Validation.resource_id == resource["id"])
            .one()
        )

        assert validation.status == "error"
        assert validation.error == {"message": ['Errors validating the data']}
        assert validation.finished

    @mock.patch(
        "ckanext.validation.jobs.validate", return_value=VALID_REPORT_LOCAL_FILE
    )
    @mock.patch.object(
        uploader, "get_resource_uploader", return_value=mock_get_resource_uploader({})
    )
    def test_job_run_uploaded_file_replaces_paths(self, mock_uploader, mock_validate):

        resource = factories.Resource(url="__upload", url_type="upload", format="csv")

        run_validation_job(resource)

        validation = (
            Session.query(Validation)
            .filter(Validation.resource_id == resource["id"])
            .one()
        )

        report = json.loads(validation.report)
        assert report["tasks"][0]["place"].startswith("http")

    @mock.patch("ckanext.validation.jobs.validate", return_value=VALID_REPORT)
    def test_job_run_valid_stores_status_in_resource(self, mock_validate):

        resource = factories.Resource(url="http://example.com/file.csv", format="csv")

        run_validation_job(resource)

        validation = (
            Session.query(Validation)
            .filter(Validation.resource_id == resource["id"])
            .one()
        )

        updated_resource = call_action("resource_show", id=resource["id"])

        assert updated_resource["validation_status"] == validation.status
        assert (
            updated_resource["validation_timestamp"] == validation.finished.isoformat()
        )

    @pytest.mark.usefixtures("mock_uploads")
    def test_job_local_paths_are_hidden(self):

        invalid_csv = "id,type\n" + "1,a,\n" * 1010
        invalid_file = get_mock_file(invalid_csv)

        mock_upload = MockFieldStorage(invalid_file, "invalid.csv")

        resource = factories.Resource(format="csv", upload=mock_upload)

        invalid_stream = io.BufferedReader(io.BytesIO(invalid_csv.encode('utf8')))

        with mock.patch("io.open", return_value=invalid_stream):
            run_validation_job(resource)

        validation = (
            Session.query(Validation)
            .filter(Validation.resource_id == resource["id"])
            .one()
        )

        report = json.loads(validation.report)
        source = report["tasks"][0]["place"]
        assert source.startswith("http")
        assert source.endswith("invalid.csv")

    @pytest.mark.usefixtures("mock_uploads")
    def test_job_pass_validation_options_string(self):

        invalid_csv = """

a;b;c
#comment
1;2;3
"""

        validation_options = """
         {
            "dialect":  {
              "header": true,
              "headerRows": [2],
              "commentChar": "#",
              "csv": {
                "delimiter": ";"
              }
            }
        }
        """

        invalid_file = get_mock_file(invalid_csv)
        mock_upload = MockFieldStorage(invalid_file, "invalid.csv")

        resource = factories.Resource(
            format="csv", upload=mock_upload, validation_options=validation_options
        )

        invalid_stream = io.BufferedReader(io.BytesIO(invalid_csv.encode('utf8')))

        with mock.patch("io.open", return_value=invalid_stream):

            run_validation_job(resource)

        validation = (
            Session.query(Validation)
            .filter(Validation.resource_id == resource["id"])
            .one()
        )

        report = json.loads(validation.report)
        assert report["valid"] is True


class TestResolveSourceUrl(object):
    """The worker must download resources from a URL it can actually reach.

    ``ckanext.validation.internal_site_url`` is the opt-in escape hatch for
    deployments where ``ckan.site_url`` is not routable from the worker.
    """

    @pytest.mark.ckan_config("ckan.site_url", "https://data.example.com")
    def test_url_is_left_alone_when_no_internal_url_configured(self):

        url = "https://data.example.com/dataset/d/resource/r/download/f.csv"

        assert _resolve_source_url(url) == url

    @pytest.mark.ckan_config("ckan.site_url", "https://data.example.com")
    @pytest.mark.ckan_config(
        "ckanext.validation.internal_site_url", "http://localhost:5000"
    )
    def test_site_url_is_swapped_for_the_internal_one(self):

        url = "https://data.example.com/dataset/d/resource/r/download/f.csv"

        assert _resolve_source_url(url) == (
            "http://localhost:5000/dataset/d/resource/r/download/f.csv"
        )

    @pytest.mark.ckan_config("ckan.site_url", "https://data.example.com/")
    @pytest.mark.ckan_config(
        "ckanext.validation.internal_site_url", "http://localhost:5000/"
    )
    def test_trailing_slashes_do_not_duplicate_the_separator(self):

        url = "https://data.example.com/dataset/d/resource/r/download/f.csv"

        assert _resolve_source_url(url) == (
            "http://localhost:5000/dataset/d/resource/r/download/f.csv"
        )

    @pytest.mark.ckan_config("ckan.site_url", "https://data.example.com")
    @pytest.mark.ckan_config(
        "ckanext.validation.internal_site_url", "http://localhost:5000"
    )
    def test_external_urls_are_not_rewritten(self):

        url = "http://example.com/file.csv"

        assert _resolve_source_url(url) == url


class MockCloudUploader(object):
    """Stands in for a cloud storage uploader.

    The point is that it is *not* a ``ckan.lib.uploader.ResourceUpload``, so
    the resource has to be downloaded over HTTP instead of read from disk.
    """

    def __init__(self, resource=None):
        pass


def mock_get_cloud_uploader(data_dict):
    return MockCloudUploader(data_dict)


@pytest.mark.usefixtures("clean_db", "validation_setup")
class TestPrivateDatasetAuthHeader(object):
    """Private resources on a cloud backend are fetched through CKAN itself,
    which needs a real API token -- the legacy ``user.apikey`` is not an
    authentication credential any more.
    """

    def _run_job_capturing_session(self, resource):

        captured = {}

        def capture(source, **kwargs):
            session = kwargs.get("http_session")
            captured["session"] = session
            if session is not None:
                header_name = ckantoolkit.config.get(
                    "apitoken_header_name", "Authorization")
                token = session.headers.get(header_name)
                captured["token"] = token
                # Resolve while the token is still alive
                user = api_token.get_user_from_token(
                    token, update_access_time=False) if token else None
                captured["user"] = user.name if user else None
            return VALID_REPORT

        with mock.patch(
            "ckanext.validation.jobs._validate_table", side_effect=capture
        ):
            run_validation_job(resource)

        return captured

    @mock.patch.object(
        uploader, "get_resource_uploader", return_value=mock_get_cloud_uploader({})
    )
    def test_token_authenticates_as_the_site_user(self, mock_uploader):

        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org["id"])
        resource = factories.Resource(
            package_id=dataset["id"], url="__upload", url_type="upload", format="csv"
        )

        captured = self._run_job_capturing_session(resource)

        site_user = call_action("get_site_user")

        assert captured["token"], "no auth header was sent"
        assert captured["user"] == site_user["name"]

    @mock.patch.object(
        uploader, "get_resource_uploader", return_value=mock_get_cloud_uploader({})
    )
    def test_token_is_revoked_when_the_job_finishes(self, mock_uploader):

        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org["id"])
        resource = factories.Resource(
            package_id=dataset["id"], url="__upload", url_type="upload", format="csv"
        )

        captured = self._run_job_capturing_session(resource)

        assert api_token.get_user_from_token(
            captured["token"], update_access_time=False) is None

    @pytest.mark.ckan_config(
        "ckanext.validation.pass_auth_header_value", "preconfigured-token"
    )
    @mock.patch.object(
        uploader, "get_resource_uploader", return_value=mock_get_cloud_uploader({})
    )
    def test_configured_header_value_is_used_as_is(self, mock_uploader):

        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org["id"])
        resource = factories.Resource(
            package_id=dataset["id"], url="__upload", url_type="upload", format="csv"
        )

        captured = self._run_job_capturing_session(resource)

        assert captured["token"] == "preconfigured-token"
        assert Session.query(ApiToken).count() == 0, "should not mint a token"

    @pytest.mark.ckan_config("ckanext.validation.pass_auth_header", False)
    @mock.patch.object(
        uploader, "get_resource_uploader", return_value=mock_get_cloud_uploader({})
    )
    def test_no_auth_header_when_turned_off(self, mock_uploader):

        org = factories.Organization()
        dataset = factories.Dataset(private=True, owner_org=org["id"])
        resource = factories.Resource(
            package_id=dataset["id"], url="__upload", url_type="upload", format="csv"
        )

        captured = self._run_job_capturing_session(resource)

        assert captured["session"] is None
        assert Session.query(ApiToken).count() == 0


class TestAuthHeaderSession(object):
    """Cloud backends redirect the CKAN download URL to a signed URL on the
    storage host. The CKAN credential must not follow it there.
    """

    def _headers_after_redirect(self, session, from_url, to_url):

        response = requests.Response()
        response.request = requests.Request("GET", from_url).prepare()
        prepared = requests.Request(
            "GET", to_url, headers=dict(session.headers)).prepare()

        session.rebuild_auth(prepared, response)

        return prepared.headers

    @pytest.mark.parametrize(
        "header_name", ["Authorization", "X-CKAN-API-TOKEN"]
    )
    def test_header_is_dropped_when_redirected_to_another_host(self, header_name):

        session = AuthHeaderSession(header_name)
        session.headers.update({header_name: "secret-token"})

        headers = self._headers_after_redirect(
            session,
            "https://data.example.com/dataset/d/resource/r/download/f.csv",
            "https://storage.example.net/signed/f.csv",
        )

        assert header_name not in headers

    @pytest.mark.parametrize(
        "header_name", ["Authorization", "X-CKAN-API-TOKEN"]
    )
    def test_header_is_kept_when_redirected_on_the_same_host(self, header_name):

        session = AuthHeaderSession(header_name)
        session.headers.update({header_name: "secret-token"})

        headers = self._headers_after_redirect(
            session,
            "https://data.example.com/dataset/d/resource/r/download/f.csv",
            "https://data.example.com/somewhere/else.csv",
        )

        assert headers[header_name] == "secret-token"
