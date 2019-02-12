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


class HTTP10Mixin(object):
    pass


class HTTP11Mixin(object):
    pass


class HTTP20Mixin(object):
    pass


class WebDAVMixin(HTTP11Mixin):
    pass


class HTCPCP10Mixin(object):
    pass


class UnofficialMixin(object):
    reference = None


class IISMixin(UnofficialMixin):
    reference = "Internet Information Services (IIS)"


class NginxMixin(UnofficialMixin):
    reference = "Nginx"


class CloudflareMixin(UnofficialMixin):
    reference = "Cloudflare"


class ErrorCodeMixin(object):
    exception = None


class StatusType(type):
    pass


class AbstractStatus(metaclass=StatusType):
    code = None
    message = ""
    category_code = ""
    category_name = ""
    category_range = None
    rfcs = ()

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, int):
            return self.code == other

        if isinstance(other, str):
            return self.message.lower() == other.lower()

        if isinstance(other, AbstractStatus):
            return self.code == other.code

        if isinstance(other, StatusType):
            return isinstance(self, other)

        return super().__eq__(other)

    def __str__(self):
        return f"{self.code} {self.message}"


class HTTPStatus(AbstractStatus):
    pass


class Informational(HTTPStatus):
    category_code = "1xx"
    category_name = "Informational"
    category_range = 100, 200


class Successful(HTTPStatus):
    category_code = "2xx"
    category_name = "Successful"
    category_range = 200, 300


class Redirection(HTTPStatus):
    category_code = "3xx"
    category_name = "Redirection"
    category_range = 300, 400


class ClientError(HTTPStatus, ErrorCodeMixin):
    category_code = "4xx"
    category_name = "Client Error"
    category_range = 400, 500


class ServerError(HTTPStatus, ErrorCodeMixin):
    category_code = "5xx"
    category_name = "Server Error"
    category_range = 500, 600
