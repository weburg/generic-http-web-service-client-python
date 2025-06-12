import types
from unittest import TestCase

from weburg.ghowst.generic_http_web_service_client import GenericHTTPWebServiceClient


class TestGenericHTTPWebServiceClient(TestCase):
    test_service = GenericHTTPWebServiceClient("http://localhost:8081/generichttpws")

    def test_create_engine(self):
        engine = types.SimpleNamespace()
        engine.name = "PythonTestEngine"
        engine.cylinders = 12
        engine.throttle_setting = 50

        engine_id = self.test_service.create_engines(engine=engine)
        self.assertTrue(engine_id > 0)