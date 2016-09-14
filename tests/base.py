import json
import unittest

import devmateclient

APPLICATION_JSON = 'application/json'


def request_as_json(pretty_request):
    return json.loads(pretty_request.body.decode("utf-8"))


class BaseApiTest(unittest.TestCase):
    def setUp(self):
        self.token = 'TEST_TOKEN'
        self.client = devmateclient.Client(self.token)

    def tearDown(self):
        self.client.close()
