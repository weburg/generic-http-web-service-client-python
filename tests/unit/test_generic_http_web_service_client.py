import types
from unittest import TestCase

from weburg.ghowst.generic_http_web_service_client import GenericHTTPWebServiceClient
from weburg.ghowst.http_web_service_exception import HttpWebServiceException


class TestGenericHTTPWebServiceClient(TestCase):
    test_service = GenericHTTPWebServiceClient("http://nohost/noservice")

    def test_create_test_resource(self):
        test_resource = types.SimpleNamespace()

        self.assertRaises(HttpWebServiceException, self.test_service.create_resource, test_resource=test_resource)