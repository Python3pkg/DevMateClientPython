import logging

from ..errors import IllegalArgumentError

PATH = '/v2/customers'
LICENSES_PATH = '/licenses'

log = logging.getLogger(__name__)


class CustomersApiMixin(object):
    def get_customer_by_id(self, customer_id, with_meta=None):
        """
        Get existing DevMate customer by given id, or error if input params are incorrect, or customer doesn't exist
        :param customer_id: `int` target customer id in DevMate
        :param with_meta: `bool` set True to return object with meta info in tuple
        :return: customer object in `dict`, or `tuple` with customer and meta info
        """
        log.debug('Get customer by id %s, with meta : %s', customer_id, with_meta)

        if customer_id is None or customer_id <= 0:
            raise IllegalArgumentError('Id should not be negative or 0. Given : {}'.format(customer_id))

        return self._dm_get(path='{}/{}'.format(PATH, customer_id), with_meta=with_meta)

    def get_customers(self,
                      with_email=None,
                      with_first_name=None,
                      with_last_name=None,
                      with_company=None,
                      with_phone=None,
                      with_address=None,
                      with_key=None,
                      with_identifier=None,
                      with_invoice=None,
                      with_order_id=None,
                      with_activation_id=None,
                      with_limit=None,
                      with_offset=None,
                      with_licenses=None,
                      with_meta=None):
        """
        Get existing DevMate customers by given filter params, or error if input params are incorrect
        :param with_email: `str` filter customer list by given email (contains)
        :param with_first_name: `str` filter customer list by given first name (contains)
        :param with_last_name: `str` filter customer list by given last name (contains)
        :param with_company: `str` filter customer list by given company name (contains)
        :param with_phone: `str` or `int` filter customer list by given phone number (contains)
        :param with_address: `str` filter customer list by given address (contains)
        :param with_key: `str` or `int` filter customer list by given activation key (equals)
        :param with_identifier: `str` or `int` filter customer list by given identifier, e.g. MAC address (contains)
        :param with_invoice: `str` or `int` filter customer list by given invoice (contains)
        :param with_order_id: `int` filter customer list by given order id (equals)
        :param with_activation_id: `int` filter customer list by given activation id (equals)
        :param with_limit: `int` max count of customers per page
        :param with_offset: `int` offset
        :param with_licenses: `bool` set True to include licenses to customer object
        :param with_meta: `bool` set True to return object with meta info in tuple
        :return: `list` of customer objects in `dict`, or `tuple` with customers and meta info
        """
        params = {
            'filter[email]': with_email,
            'filter[first_name]': with_first_name,
            'filter[last_name]': with_last_name,
            'filter[company]': with_company,
            'filter[phone]': with_phone,
            'filter[address]': with_address,
            'filter[key]': with_key,
            'filter[identifier]': with_identifier,
            'filter[order_id]': with_order_id,
            'filter[activation_id]': with_activation_id,
            'filter[invoice]': with_invoice,
            'offset': with_offset,
            'limit': with_limit,
            'with': 'licenses' if with_licenses else None
        }

        log.debug('Get customers with params %s, with meta : %s', params, with_meta)

        not_none_params = dict((k, v) for k, v in list(params.items()) if v is not None)

        return self._dm_get(path=PATH, params=not_none_params, with_meta=with_meta)

    def create_customer(self, customer, with_meta=None):
        """
        Create new customer in DevMate, or error if input params are incorrect
        :param customer: customer data in `dict`, 'email' field should be set in `dict`
        :param with_meta: `bool` set True to return object with meta info in tuple
        :return: created customer object in `dict`, or `tuple` with customer and meta info
        """
        log.debug('Create customer with details %s, with meta : %s', customer, with_meta)

        if 'email' not in customer or customer['email'] is None:
            raise IllegalArgumentError('"email" field should be set for the customer')

        return self._dm_post(path=PATH, json={'data': customer}, with_meta=with_meta)

    def update_customer(self, customer, with_meta=None):
        """
        Update existing customer in DevMate, or error if input params are incorrect, or customer doesn't exist
        :param customer: updated customer data in `dict`, 'id' field should be set in `dict`
        :param with_meta: `bool` set True to return object with meta info in tuple
        :return: created customer object in `dict`, or `tuple` with customer and meta info
        """
        log.debug('Update customer with details %s, with meta : %s', customer, with_meta)

        if 'id' not in customer or customer['id'] is None:
            raise IllegalArgumentError('Current customer "id" field should be set for the customer')

        return self._dm_put(path='{}/{}'.format(PATH, customer['id']), json={'data': customer}, with_meta=with_meta)

    def create_license_for_customer(self, customer_id, _license, with_meta=None):
        """
        Create new license for existing customer in DevMate by license type id,
        or error if input params are incorrect, or customer doesn't exist
        :param customer_id: `int` id of customer in DevMate
        :param _license: license object in `dict`, 'license_type_id' field should be set in `dict`
        :param with_meta: `bool` set True to return object with meta info in tuple
        :return: created license object in `dict`, or `tuple` with license and meta info
        """
        log.debug('Create license for customer %s with details %s, with meta : %s', customer_id, _license, with_meta)

        if customer_id is None or customer_id <= 0:
            raise IllegalArgumentError('Id should not be negative or 0. Given : {}'.format(customer_id))

        if 'license_type_id' not in _license or _license['license_type_id'] is None:
            raise IllegalArgumentError('Current customer "license_type_id" field should be set for the customer')

        return self._dm_post(
            path='{}/{}{}'.format(PATH, customer_id, LICENSES_PATH),
            json={'data': _license},
            with_meta=with_meta
        )
