from weburg.ghowst.http_web_service_invoker import *


# Thin wrapper for stubless client
class GenericHTTPWebServiceClient:
    __base_url = ''
    __http_web_service_invoker = None

    def __init__(self, base_url):
        self.__base_url = base_url
        self.__http_web_service_invoker = HTTPWebServiceInvoker()

    def __getattr__(self, name):
        def dynamic_method(**arguments):
            return self.__http_web_service_invoker.invoke(name, arguments, self.__base_url)

        return dynamic_method
