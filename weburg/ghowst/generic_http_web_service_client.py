from weburg.ghowst.http_web_service_invoker import *


# Thin wrapper for stubless client
class GenericHTTPWebServiceClient:
    base_url = ''
    http_web_service_invoker = None

    # Public

    def __init__(self, base_url):
        self.base_url = base_url
        self.http_web_service_invoker = HTTPWebServiceInvoker()

    def __getattr__(self, name):
        def dynamic_method(**arguments):
            return self.http_web_service_invoker.invoke(name, arguments, self.base_url)

        return dynamic_method