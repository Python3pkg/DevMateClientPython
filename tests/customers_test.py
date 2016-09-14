import json
import httpretty

from devmateclient import consts
from devmateclient import errors
from devmateclient.client import BASE_URL
from .base import BaseApiTest, APPLICATION_JSON, request_as_json

DEFAULT_CUSTOMER = {
    'id': 1,
    'email': 'test@email.com',
    'first_name': 'First',
    'last_name': 'Second',
    'company': 'Company',
    'phone': '+1234567890',
    'address': 'Test Address',
    'note': 'Test Note',
    'dateAdded': 1471478400
}

DEFAULT_LICENSE = {
    'id': 1,
    'campaign': 'Test Campaign',
    'status': consts.LicenseStatus.ACTIVE,
    'license_type_id': 1,
    'license_type_name': 'Test License Type',
    'invoice': 'Test Invoice',
    'activations_total': 100,
    'activations_used': 50,
    'activation_key': 'id123456789098odr',
    'is_subscription': True,
    'date_created': 1471478400,
    'expiration_date': 1471478400,
    'products': [{
        'id': 1,
        'name': 'Test Product',
        'bundle_id': 'com.test.bundle',
        'use_offline_license': True
    }],
    'history': [{
        'type': consts.HistoryRecordType.ACTIVATION,
        'user_name': 'Test User',
        'note': 'Test Note',
        'timestamp': 1471478400,
        'id': 1,
        'license_id': 1,
        'activation_id': 1,
        'activation_name': 'Act Name',
        'activation_email': 'act@mail.test',
        'offline_license': 'Offline',
        'product_name': 'Test Product',
        'identifiers': 'aa:aa:aa:aa:aa:aa',
        'deactivated': 1
    }]
}


def customer_with_license():
    d = dict(DEFAULT_CUSTOMER)
    d['licenses'] = dict(DEFAULT_LICENSE)
    return d


class CustomersTest(BaseApiTest):
    @httpretty.activate
    def test_get_customer_by_id(self):
        httpretty.register_uri(
            method=httpretty.GET,
            uri=BASE_URL + '/v2/customers/1',
            status=200,
            content_type=APPLICATION_JSON,
            body=json.dumps({'data': DEFAULT_CUSTOMER})
        )

        customer = self.client.get_customer_by_id(1)

        self.assertDictEqual(customer, DEFAULT_CUSTOMER)

    def test_get_customer_by_negative_id(self):
        with self.assertRaises(errors.IllegalArgumentError):
            self.client.get_customer_by_id(-1)

    def test_get_customer_by_zero_id(self):
        with self.assertRaises(errors.IllegalArgumentError):
            self.client.get_customer_by_id(0)

    @httpretty.activate
    def test_get_customers(self):
        expected_customers = [customer_with_license()]

        httpretty.register_uri(
            method=httpretty.GET,
            uri=BASE_URL + '/v2/customers',
            status=200,
            content_type=APPLICATION_JSON,
            body=json.dumps({'data': expected_customers})
        )

        customers = self.client.get_customers(with_email='email',
                                              with_first_name='first_name',
                                              with_last_name='last_name',
                                              with_company='company',
                                              with_phone='1234567890',
                                              with_address='address',
                                              with_identifier='aa:aa:aa:aa:aa:aa',
                                              with_invoice='invoice',
                                              with_key='1234567890',
                                              with_activation_id=1234567890,
                                              with_order_id=1234567890,
                                              with_limit=20,
                                              with_offset=20,
                                              with_licenses=True)

        self.assertEqual(customers, expected_customers)
        self.assertEqual(httpretty.last_request().querystring, {
            'filter[email]': ['email'],
            'filter[first_name]': ['first_name'],
            'filter[last_name]': ['last_name'],
            'filter[company]': ['company'],
            'filter[phone]': ['1234567890'],
            'filter[address]': ['address'],
            'filter[identifier]': ['aa:aa:aa:aa:aa:aa'],
            'filter[invoice]': ['invoice'],
            'filter[key]': ['1234567890'],
            'filter[activation_id]': ['1234567890'],
            'filter[order_id]': ['1234567890'],
            'offset': ['20'],
            'limit': ['20'],
            'with': ['licenses']
        })

    @httpretty.activate
    def test_create_customer(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/v2/customers',
            status=201,
            content_type=APPLICATION_JSON,
            body=json.dumps({'data': DEFAULT_CUSTOMER})
        )

        customer = self.client.create_customer(DEFAULT_CUSTOMER)

        self.assertDictEqual(customer, DEFAULT_CUSTOMER)
        self.assertDictEqual(request_as_json(httpretty.last_request()), {'data': DEFAULT_CUSTOMER})

    def test_create_customer_without_email(self):
        with self.assertRaises(errors.IllegalArgumentError):
            self.client.create_customer({})

    @httpretty.activate
    def test_update_customer(self):
        httpretty.register_uri(
            method=httpretty.PUT,
            uri=BASE_URL + '/v2/customers/1',
            status=200,
            content_type=APPLICATION_JSON,
            body=json.dumps({'data': DEFAULT_CUSTOMER})
        )

        customer = self.client.update_customer(DEFAULT_CUSTOMER)

        self.assertDictEqual(customer, DEFAULT_CUSTOMER)
        self.assertDictEqual(request_as_json(httpretty.last_request()), {'data': DEFAULT_CUSTOMER})

    def test_update_customer_without_id(self):
        with self.assertRaises(errors.IllegalArgumentError):
            self.client.update_customer({})

    @httpretty.activate
    def test_create_license_for_customer(self):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/v2/customers/1/licenses',
            status=201,
            content_type=APPLICATION_JSON,
            body=json.dumps({'data': DEFAULT_LICENSE})
        )

        _license = self.client.create_license_for_customer(customer_id=1, _license={'license_type_id': 1})

        self.assertEqual(_license, DEFAULT_LICENSE)
        self.assertDictEqual(request_as_json(httpretty.last_request()), {'data': {'license_type_id': 1}})

    def test_create_license_for_customer_with_negative_id(self):
        with self.assertRaises(errors.IllegalArgumentError):
            self.client.create_license_for_customer(customer_id=-1, _license={})

    def test_create_license_for_customer_with_zero_id(self):
        with self.assertRaises(errors.IllegalArgumentError):
            self.client.create_license_for_customer(customer_id=0, _license={})

    def test_create_license_for_customer_without_license_type_id(self):
        with self.assertRaises(errors.IllegalArgumentError):
            self.client.create_license_for_customer(customer_id=1, _license={})
