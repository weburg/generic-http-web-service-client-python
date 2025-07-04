import types
from unittest import TestCase

from weburg.ghowst.generic_http_web_service_client import GenericHTTPWebServiceClient
from weburg.ghowst.http_web_service_exception import HttpWebServiceException


class TestGenericHTTPWebServiceClient(TestCase):
    test_service = GenericHTTPWebServiceClient("http://nohost/noservice")

    def test_service_exception(self):
        engine = types.SimpleNamespace()
        engine.name = "PythonTestEngine"
        engine.cylinders = 12
        engine.throttle_setting = 50

        self.assertRaises(HttpWebServiceException, self.test_service.create_engines, engine=engine)