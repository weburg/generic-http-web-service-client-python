import _io
import json
import urllib.parse
import requests
from types import SimpleNamespace


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

        if verb == "get":
            uriStr = base_url + '/' + entity + self._generate_qs(arguments)

            result = requests.get(uriStr, headers={"accept": "application/json"})

            if result.status_code == 200:
                return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
            else:
                raise RuntimeError(f"HTTP {result.status_code} when requesting {uriStr}")
        elif verb == "create":
            uriStr = base_url + '/' + entity

            files = {}
            values = {}

            for name, value in arguments.items():
                for property in vars(value):
                    if type(value.__dict__[property]) == _io.BufferedReader:
                        # Field type is a File
                        files[self._underbar_to_camel(property)] = (value.__dict__[property].name, value.__dict__[property])
                    else:
                        # Field type is normal / text
                        values[self._underbar_to_camel(property)] = value.__dict__[property]

            result = requests.post(uriStr, files=files, data=values, headers={"accept": "application/json"})

            if result.status_code == 200 or result.status_code == 201:
                return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
            else:
                raise RuntimeError(f"HTTP {result.status_code} when requesting {uriStr}")
        elif verb == "create_or_replace":
            uriStr = base_url + '/' + entity

            files = {}
            values = {}

            for name, value in arguments.items():
                for property in vars(value):
                    if type(value.__dict__[property]) == _io.BufferedReader:
                        # Field type is a File
                        files[self._underbar_to_camel(property)] = (value.__dict__[property].name, value.__dict__[property])
                    else:
                        # Field type is normal / text
                        values[self._underbar_to_camel(property)] = value.__dict__[property]

            result = requests.put(uriStr, files=files, data=values, headers={"accept": "application/json"})

            if result.status_code == 200 or result.status_code == 201:
                return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))
            else:
                raise RuntimeError(f"HTTP {result.status_code} when requesting {uriStr}")
        elif verb == "update":
            uriStr = base_url + '/' + entity

            files = {}
            values = {}

            for name, value in arguments.items():
                for property in vars(value):
                    if type(value.__dict__[property]) == _io.BufferedReader:
                        # Field type is a File
                        files[self._underbar_to_camel(property)] = (value.__dict__[property].name, value.__dict__[property])
                    else:
                        # Field type is normal / text
                        values[self._underbar_to_camel(property)] = value.__dict__[property]

            result = requests.patch(uriStr, files=files, data=values, headers={"accept": "application/json"})

            if result.status_code == 200 or result.status_code == 201:
                return None
            else:
                raise RuntimeError(f"HTTP {result.status_code} when requesting {uriStr}")
        elif verb == "delete":
            uriStr = base_url + '/' + entity + self._generate_qs(arguments)

            result = requests.delete(uriStr, headers={"accept": "application/json"})

            if result.status_code == 200:
                return None
            else:
                raise RuntimeError(f"HTTP {result.status_code} when requesting {uriStr}")
        else:
            # POST to a custom verb resource

            uriStr = base_url + '/' + entity + '/' + verb

            values = {}

            for name, value in arguments.items():
                values[self._underbar_to_camel(name)] = value

            result = requests.post(uriStr, data=values, headers={"accept": "application/json"})

            if result.status_code == 200 or result.status_code == 201:
                return None
            else:
                raise RuntimeError(f"HTTP {result.status_code} when requesting {uriStr}")