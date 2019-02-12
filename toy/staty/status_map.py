# Copyright 2016 Osvaldo Santana Neto <staty@osantana.me>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from staty import exceptions, base
from staty.utils import camel2snake


class HTTPStatusMap:
    def __init__(self):
        self.codes = {}
        self.errors = {}
        self.attribute_names = {}
        self.exceptions = {}

    def __getattr__(self, item):
        try:
            return self.attribute_names[item]
        except KeyError as exc:
            raise AttributeError("{!r} object has no attribute {!r}".format(self.__class__.__name__, item)) from exc

    def __getitem__(self, item):
            return self.codes[item]

    def register(self, http_status_class):
        code = http_status_class.code
        name = http_status_class.__name__

        if code in self.codes:
            raise exceptions.RegistrationException("Status code is already registered")

        http_status = http_status_class()
        self.codes[code] = http_status

        if issubclass(http_status_class, base.ErrorCodeMixin):
            self.errors[code] = http_status

        if hasattr(http_status_class, 'exception'):
            self.exceptions[http_status_class.exception] = http_status

        name = camel2snake(name, upper=True)

        status_name = "HTTP_{}_{}".format(code, name)
        self.attribute_names[status_name] = http_status

        return http_status_class


status = HTTPStatusMap()
