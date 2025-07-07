import _io
import json
import logging
import urllib.parse
from json import JSONDecodeError
from types import SimpleNamespace

import requests

from weburg.ghowst.http_web_service_exception import HttpWebServiceException


class HTTPWebServiceInvoker:
    @staticmethod
    def __get_resource_name(name, verb):
        return name[len(verb) + 1 : len(name)].lower()

    @staticmethod
    def __underbar_to_camel(string):
        new_string = ''

        upper_next = False
        for char in string:
            if char == '_':
                upper_next = True
                continue

            if upper_next:
                new_string += char.upper()
                upper_next = False
            else:
                new_string += char

        return new_string

    @staticmethod
    def __camel_to_underbar(string):
        new_string = ''

        for char in string:
            if new_string != '' and char == char.upper():
                new_string += "_#{char.lower()}"
            else:
               new_string += char.lower()

        return new_string

    @staticmethod
    def __generate_qs(arguments):
        return ('?' + urllib.parse.urlencode(arguments) if len(arguments) > 0 else "")

    @staticmethod
    def __has_user_properties(value):
        if hasattr(value, "__dict__"):
            for property in vars(value):
                if not property.startswith("__"):
                    return True
        return False

    @staticmethod
    def __handle_result(result):
        if result.status_code >= 400 or result.status_code < 200:
            raise HttpWebServiceException(result.status_code, result.headers["x-error-message"])
        elif result.status_code >= 300 and result.status_code < 400:
            raise HttpWebServiceException(result.status_code, result.headers["location"])

        try:
            return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
        except JSONDecodeError:
            return None

    def __http_entity_from_arguments(self, arguments):
        values = {}
        files = {}

        for name, value in arguments.items():
            if not self.__has_user_properties(value):
                if type(value) == _io.BufferedReader:
                    files[self.__underbar_to_camel(name)] = value
                else:
                    values[self.__underbar_to_camel(name)] = value
            else:
                for property in vars(value):
                    if type(value.__dict__[property]) == _io.BufferedReader:
                        files[self.__underbar_to_camel(name) + '.' + self.__underbar_to_camel(property)] = (
                            value.__dict__[property].name, value.__dict__[property]
                        )
                    elif not property.startswith("__"):
                        values[self.__underbar_to_camel(name) + '.' + self.__underbar_to_camel(property)] = (
                            value.__dict__[property]
                        )

        return values, files

    def invoke(self, method_name, arguments, base_url):
        if method_name.startswith("get"):
            verb = "get"
            resource = self.__get_resource_name(method_name, verb)
        elif method_name.startswith("create_or_replace"):
            verb = "create_or_replace"
            resource = self.__get_resource_name(method_name, verb)
        elif method_name.startswith("create"):
            verb = "create"
            resource = self.__get_resource_name(method_name, verb)
        elif method_name.startswith("update"):
            verb = "update"
            resource = self.__get_resource_name(method_name, verb)
        elif method_name.startswith("delete"):
            verb = "delete"
            resource = self.__get_resource_name(method_name, verb)
        else:
            parts = method_name.split('_')

            verb = parts[0].lower()
            resource = self.__get_resource_name(method_name, verb)

        logging.info(f"Verb: {verb}")
        logging.info(f"Resource: {resource}")

        headers = {"accept": "application/json"}

        try:
            if verb == "get":
                uri_str = base_url + '/' + resource + self.__generate_qs(arguments)

                result = requests.get(uri_str, headers=headers)

                return self.__handle_result(result)
            elif verb == "create":
                uri_str = base_url + '/' + resource

                values, files = self.__http_entity_from_arguments(arguments)

                result = requests.post(uri_str, data=values, files=files, headers=headers)

                return self.__handle_result(result)
            elif verb == "create_or_replace":
                uri_str = base_url + '/' + resource

                values, files = self.__http_entity_from_arguments(arguments)

                result = requests.put(uri_str, data=values, files=files, headers=headers)

                return self.__handle_result(result)
            elif verb == "update":
                uri_str = base_url + '/' + resource

                values, files = self.__http_entity_from_arguments(arguments)

                result = requests.patch(uri_str, data=values, files=files, headers=headers)

                return self.__handle_result(result)
            elif verb == "delete":
                uri_str = base_url + '/' + resource + self.__generate_qs(arguments)

                result = requests.delete(uri_str, headers=headers)

                return self.__handle_result(result)
            else:
                # POST to a custom verb resource

                uri_str = base_url + '/' + resource + '/' + verb

                values, files = self.__http_entity_from_arguments(arguments)

                result = requests.post(uri_str, data=values, files=files, headers=headers)

                return self.__handle_result(result)
        except HttpWebServiceException as e:
            raise e
        except Exception as e:
            raise HttpWebServiceException(0, "There was a problem processing the web service request: " + str(e))