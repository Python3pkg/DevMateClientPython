import logging

import requests

from . import api
from . import errors

BASE_URL = 'https://public-api.devmate.com'

log = logging.getLogger(__name__)


class Client(requests.Session, api.CustomersApiMixin, api.LicensesApiMixin):
    """
    DevMate Public API client.
    To initialize this you have to set auth_token, which can be generated in Settings -> API Integration.
    You can change auth token in runtime with auth_token property.
    """
    def __init__(self, auth_token):
        super(Client, self).__init__()
        self._auth_token = auth_token
        self._base_url = BASE_URL

    @property
    def auth_token(self):
        return self._auth_token

    @auth_token.setter
    def auth_token(self, auth_token):
        self._auth_token = auth_token

    def _url(self, path):
        return '{base_url}{path}'.format(base_url=self._base_url, path=path)

    def _add_auth_header(self, req_kwargs):
        if self._auth_token is not None:
            log.debug('Add auth token %s to header with request params %s', self._auth_token, req_kwargs)

            token_header = {'Authorization': 'Token {}'.format(self._auth_token)}

            if not req_kwargs.get('headers'):
                req_kwargs['headers'] = token_header
            else:
                req_kwargs['headers'].update(token_header)

    @staticmethod
    def _check_dm_errors(response):
        log.debug('Check errors for response %s', response)

        if 200 <= response.status_code < 300:
            return
        elif response.status_code == 400:
            error = errors.IncorrectParamsError(response)
        elif response.status_code == 404:
            error = errors.NotFoundError(response)
        elif response.status_code == 409:
            error = errors.ConflictError(response)
        elif 400 <= response.status_code < 500:
            error = errors.DevMateClientError(response)
        elif 500 <= response.status_code < 600:
            error = errors.DevMateServerError(response)
        else:
            error = errors.DevMateRequestError(response)

        try:
            json = response.json()
            error.dm_errors = json['errors']
        except Exception:
            error.dm_errors = []

        raise error

    @staticmethod
    def _is_application_json(headers):
        return 'Content-Type' in headers and headers['Content-Type'] == 'application/json'

    def _extract_data(self, response, with_meta):
        log.debug('Extract data from response %s, with meta : %s', response, with_meta)

        if not self._is_application_json(response.headers):
            log.debug('Response doesn\'t contain JSON, return response %s', response)
            return response

        try:
            json = response.json()

            if 'data' not in json:
                log.debug('Return whole JSON %s', json)
                return json

            if with_meta:
                data = json['data']
                meta = json['meta'] if 'meta' in json else None
                log.debug('Return JSON data %s and meta %s', data, meta)
                return data, meta
            else:
                data = json['data']
                log.debug('Return JSON data %s', data)
                return data
        except Exception as e:
            log.debug('Error on parsing json %s, return response', e, response)
            return response

    def _dm_request(self, method, path, with_meta, **kwargs):
        url = self._url(path)
        self._add_auth_header(kwargs)
        log.debug('Send %s request to %s with args %s', method, url, kwargs)
        response = self.request(method=method, url=url, **kwargs)
        self._check_dm_errors(response)
        return self._extract_data(response, with_meta=with_meta)

    def _dm_get(self, path, with_meta, **kwargs):
        return self._dm_request('GET', path, with_meta, **kwargs)

    def _dm_post(self, path, with_meta, **kwargs):
        return self._dm_request('POST', path, with_meta, **kwargs)

    def _dm_put(self, path, with_meta, **kwargs):
        return self._dm_request('PUT', path, with_meta, **kwargs)
