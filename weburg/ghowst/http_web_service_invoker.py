import _io
import json
import urllib.parse
from json import JSONDecodeError
from types import SimpleNamespace

import requests

from weburg.ghowst.http_web_service_exception import HttpWebServiceException


class HTTPWebServiceInvoker:
    @staticmethod
    def _get_entity_name(name, verb):
        return name[len(verb) + 1 : len(name)].lower()

    @staticmethod
    def _underbar_to_camel(string):
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
    def _camel_to_underbar(string):
        new_string = ''

        for char in string:
            if new_string != '' and char == char.upper():
                new_string += "_#{char.lower()}"
            else:
               new_string += char.lower()

        return new_string

    @staticmethod
    def _generate_qs(arguments):
        return ('?' + urllib.parse.urlencode(arguments) if len(arguments) > 0 else "")

    @staticmethod
    def _has_user_properties(value):
        if hasattr(value, "__dict__"):
            for property in vars(value):
                if not property.startswith("__"):
                    return True
        return False

    def invoke(self, method_name, arguments, base_url):
        if method_name.startswith("get"):
            verb = "get"
            entity = self._get_entity_name(method_name, verb)
        elif method_name.startswith("create_or_replace"):
            verb = "create_or_replace"
            entity = self._get_entity_name(method_name, verb)
        elif method_name.startswith("create"):
            verb = "create"
            entity = self._get_entity_name(method_name, verb)
        elif method_name.startswith("update"):
            verb = "update"
            entity = self._get_entity_name(method_name, verb)
        elif method_name.startswith("delete"):
            verb = "delete"
            entity = self._get_entity_name(method_name, verb)
        else:
            parts = method_name.split('_')

            verb = parts[0].lower()
            entity = self._get_entity_name(method_name, verb)

        print(f"Verb: {verb}")
        print(f"Entity: {entity}")

        try:
            if verb == "get":
                uri_str = base_url + '/' + entity + self._generate_qs(arguments)

                result = requests.get(uri_str, headers={"accept": "application/json"})

                if result.status_code >= 400 or result.status_code < 200:
                    raise HttpWebServiceException(result.status_code, result.headers["x-error-message"])
                elif result.status_code >= 300 and result.status_code < 400:
                    raise HttpWebServiceException(result.status_code, result.headers["location"])

                return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
            elif verb == "create":
                uri_str = base_url + '/' + entity

                files = {}
                values = {}

                for name, value in arguments.items():
                    for property in vars(value):
                        if type(value.__dict__[property]) == _io.BufferedReader:
                            # Field type is a File
                            files[self._underbar_to_camel(property)] = (value.__dict__[property].name, value.__dict__[property])
                        elif not property.startswith("__"):
                            # Field type is normal / text
                            values[self._underbar_to_camel(property)] = value.__dict__[property]

                result = requests.post(uri_str, files=files, data=values, headers={"accept": "application/json"})

                if result.status_code >= 400 or result.status_code < 200:
                    raise HttpWebServiceException(result.status_code, result.headers["x-error-message"])
                elif result.status_code >= 300 and result.status_code < 400:
                    raise HttpWebServiceException(result.status_code, result.headers["location"])

                return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
            elif verb == "create_or_replace":
                uri_str = base_url + '/' + entity

                files = {}
                values = {}

                for name, value in arguments.items():
                    for property in vars(value):
                        if type(value.__dict__[property]) == _io.BufferedReader:
                            # Field type is a File
                            files[self._underbar_to_camel(property)] = (value.__dict__[property].name, value.__dict__[property])
                        elif not property.startswith("__"):
                            # Field type is normal / text
                            values[self._underbar_to_camel(property)] = value.__dict__[property]

                result = requests.put(uri_str, files=files, data=values, headers={"accept": "application/json"})

                if result.status_code >= 400 or result.status_code < 200:
                    raise HttpWebServiceException(result.status_code, result.headers["x-error-message"])
                elif result.status_code >= 300 and result.status_code < 400:
                    raise HttpWebServiceException(result.status_code, result.headers["location"])

                return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
            elif verb == "update":
                uri_str = base_url + '/' + entity

                files = {}
                values = {}

                for name, value in arguments.items():
                    for property in vars(value):
                        if type(value.__dict__[property]) == _io.BufferedReader:
                            # Field type is a File
                            files[self._underbar_to_camel(property)] = (value.__dict__[property].name, value.__dict__[property])
                        elif not property.startswith("__"):
                            # Field type is normal / text
                            values[self._underbar_to_camel(property)] = value.__dict__[property]

                result = requests.patch(uri_str, files=files, data=values, headers={"accept": "application/json"})

                if result.status_code >= 400 or result.status_code < 200:
                    raise HttpWebServiceException(result.status_code, result.headers["x-error-message"])
                elif result.status_code >= 300 and result.status_code < 400:
                    raise HttpWebServiceException(result.status_code, result.headers["location"])

                return None
            elif verb == "delete":
                uri_str = base_url + '/' + entity + self._generate_qs(arguments)

                result = requests.delete(uri_str, headers={"accept": "application/json"})

                if result.status_code >= 400 or result.status_code < 200:
                    raise HttpWebServiceException(result.status_code, result.headers["x-error-message"])
                elif result.status_code >= 300 and result.status_code < 400:
                    raise HttpWebServiceException(result.status_code, result.headers["location"])

                return None
            else:
                # POST to a custom verb resource

                uri_str = base_url + '/' + entity + '/' + verb

                values = {}

                for name, value in arguments.items():
                    if not self._has_user_properties(value):
                        values[self._underbar_to_camel(name)] = value
                    else:
                        for property in vars(value):
                            values[self._underbar_to_camel(name) + '.' + self._underbar_to_camel(property)] = value.__dict__[property]

                result = requests.post(uri_str, data=values, headers={"accept": "application/json"})

                if result.status_code >= 400 or result.status_code < 200:
                    raise HttpWebServiceException(result.status_code, result.headers["x-error-message"])
                elif result.status_code >= 300 and result.status_code < 400:
                    raise HttpWebServiceException(result.status_code, result.headers["location"])

                try:
                    return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
                except JSONDecodeError:
                    return None
        except HttpWebServiceException as e:
            raise e
        except Exception as e:
            raise HttpWebServiceException(500, "There was a problem processing the web service request: " + str(e))
