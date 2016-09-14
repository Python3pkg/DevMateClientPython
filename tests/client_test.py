import json

import httpretty

from devmateclient.client import BASE_URL
from devmateclient import errors
from .base import BaseApiTest, APPLICATION_JSON


class FakeResponse(object):
    def __init__(self, status_code=200, headers=None, _json=None):
        self.status_code = status_code
        self.headers = headers or {}
        self._json = _json

    def json(self):
        return self._json


class ClientTest(BaseApiTest):
    def test_url(self):
        path = '/some_path'
        self.assertEqual(self.client._url(path=path), BASE_URL + path)

    def test_add_auth_header_with_headers(self):
        args = {'headers': {'dead': 'beef'}}
        self.client._add_auth_header(args)
        self.assertDictEqual(args, {'headers': {
            'Authorization': 'Token {}'.format(self.token),
            'dead': 'beef'
        }})

    def test_add_auth_header_with_no_headers_given(self):
        args = {}
        self.client._add_auth_header(args)
        self.assertDictEqual(args, {'headers': {'Authorization': 'Token {}'.format(self.token)}})

    def test_check_dm_errors_success_200(self):
        self.client._check_dm_errors(response=FakeResponse(status_code=200))

    def test_check_dm_errors_success_299(self):
        self.client._check_dm_errors(response=FakeResponse(status_code=299))

    def test_check_dm_errors_incorrect_params_error(self):
        with self.assertRaises(errors.IncorrectParamsError):
            self.client._check_dm_errors(response=FakeResponse(status_code=400))

    def test_check_dm_errors_not_found_error(self):
        with self.assertRaises(errors.NotFoundError):
            self.client._check_dm_errors(response=FakeResponse(status_code=404))

    def test_check_dm_errors_conflict_error(self):
        with self.assertRaises(errors.ConflictError):
            self.client._check_dm_errors(response=FakeResponse(status_code=409))

    def test_check_dm_errors_client_error(self):
        with self.assertRaises(errors.DevMateClientError):
            self.client._check_dm_errors(response=FakeResponse(status_code=499))

    def test_check_dm_errors_server_error(self):
        with self.assertRaises(errors.DevMateServerError):
            self.client._check_dm_errors(response=FakeResponse(status_code=500))

    def test_check_dm_errors_request_error(self):
        with self.assertRaises(errors.DevMateRequestError):
            self.client._check_dm_errors(response=FakeResponse(status_code=300))

    def test_check_dm_errors_details(self):
        expected_errors = [{
            'title': 'test_title',
            'detail': 'test_detail'
        }]

        response = FakeResponse(status_code=300, _json={'errors': expected_errors})

        with self.assertRaises(errors.DevMateRequestError) as c:
            self.client._check_dm_errors(response=response)

        self.assertEqual(c.exception.dm_errors, expected_errors)

    def test_extract_data_not_json(self):
        data = self.client._extract_data(response=FakeResponse(), with_meta=False)
        self.assertIsInstance(data, FakeResponse)

    def test_extract_data_without_meta(self):
        expected_data = {'dead': 'beef'}
        response = FakeResponse(headers={'Content-Type': APPLICATION_JSON}, _json={'data': expected_data})

        data = self.client._extract_data(response=response, with_meta=False)

        self.assertDictEqual(data, expected_data)

    def test_extract_data_with_meta(self):
        expected_data = {'dead': 'beef'}
        expected_meta = {'beef': 'dead'}
        response = FakeResponse(headers={'Content-Type': APPLICATION_JSON}, _json={
            'data': expected_data,
            'meta': expected_meta
        })

        data, meta = self.client._extract_data(response=response, with_meta=True)

        self.assertDictEqual(data, expected_data)
        self.assertDictEqual(meta, expected_meta)

    def test_extract_data_with_no_data_field(self):
        expected = {'dead': 'beef'}
        response = FakeResponse(headers={'Content-Type': APPLICATION_JSON}, _json=expected)

        data = self.client._extract_data(response=response, with_meta=False)

        self.assertDictEqual(data, expected)

    @httpretty.activate
    def test_dm_request(self):
        json_body = {'data': {'json': True}, 'meta': {'meta_data': 'deadbeef'}}

        httpretty.register_uri(
            method=httpretty.GET,
            uri=BASE_URL + '/',
            status=200,
            content_type=APPLICATION_JSON,
            body=json.dumps(json_body)
        )

        data, meta = self.client._dm_request(
            method='GET',
            path='/',
            with_meta=True
        )

        self.assertEqual(data, json_body['data'])
        self.assertEqual(meta, json_body['meta'])
        self.assertEqual(httpretty.last_request().headers.get('Authorization'), 'Token ' + self.token)
