import httpretty

from devmateclient.client import BASE_URL
from .base import APPLICATION_JSON, BaseApiTest


class CustomersTest(BaseApiTest):
    @httpretty.activate
    def test_reset_first_activation(self):
        key = 'id123456789098odr'

        httpretty.register_uri(
            method=httpretty.POST,
            uri=BASE_URL + '/v2/licenses/' + key + '/reset_first_activation',
            status=200,
            content_type=APPLICATION_JSON,
            body=''
        )

        self.client.reset_first_activation(key)
