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


import warnings
from functools import wraps

from .. import exceptions
from staty import status

try:
    from requests import exceptions as request_exceptions
except ImportError:
    warnings.warn("missing requests library", ImportWarning)  # pragma: nocover
    request_exceptions = None  # pragma: nocover


def raise_for_status(response):
    if response.status_code in status.errors:
        status_class = status.errors[response.status_code]
        raise status_class.exception(response=response)

    return response


class RequestSessionWrapper:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, item):
        attr = getattr(self.wrapped, item)
        if not callable(attr):
            return attr

        @wraps(attr)
        def wrapper(*args, **kwargs):
            try:
                return attr(*args, **kwargs)
            except request_exceptions.Timeout as exc:
                raise exceptions.ConnectionTimeoutException() from exc

        return wrapper


def wrap(session):
    return RequestSessionWrapper(session)
