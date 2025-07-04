import os
import subprocess
from unittest import TestCase


os.chdir(os.path.dirname(os.path.abspath(__file__)))

class TestExampleGenericHttpWebServiceClient(TestCase):
    def test_example_generic_http_web_service_client(self):
        returnValue = subprocess.call(["python", "run_example_generic_http_web_service_client.py"], cwd="../../")
        self.assertTrue(returnValue == 0)