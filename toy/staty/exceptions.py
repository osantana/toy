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


# noinspection PyPep8Naming
from socket import gaierror as SocketNameResolutionError, herror as SocketHostError, timeout as SocketTimeout

from .status_map import status


# Base Exceptions & Mixins
# ========================


class StatyBaseException(Exception):
    pass


class RecoverableErrorMixin(Exception):
    pass


class UnrecoverableErrorMixin(Exception):
    pass


class RegistrationException(StatyBaseException):
    pass


class MissingHandlerException(StatyBaseException):
    pass


class HTTPError(StatyBaseException):
    def __init__(self, *args, response=None, request=None):
        self.response = response
        self.request = request
        if self.request is None and self.response is not None:
            self.request = getattr(self.response, "request", None)
        super().__init__(*args)

    @property
    def status(self):
        return status.exceptions[self.__class__]


# Connection Errors
# =================

class ConnectionException(StatyBaseException):
    pass


class ConnectionTimeoutException(SocketTimeout, ConnectionException, RecoverableErrorMixin):
    pass


class NameResolutionException(SocketNameResolutionError, ConnectionException, RecoverableErrorMixin):
    pass


class HostAddressException(SocketHostError, ConnectionException, RecoverableErrorMixin):
    pass


class SSLException(ConnectionException, RecoverableErrorMixin):
    pass


class ProxyException(ConnectionException, RecoverableErrorMixin):
    pass


# HTTP Client Errors
# ==================

class ClientErrorException(HTTPError):
    pass


class RecoverableClientErrorException(ClientErrorException, RecoverableErrorMixin):
    pass


class UnrecoverableClientErrorException(ClientErrorException, UnrecoverableErrorMixin):
    pass


class PreconditionRequiredException(UnrecoverableClientErrorException):
    pass


class TooManyRequestsException(RecoverableClientErrorException):
    pass


class BadRequestException(UnrecoverableClientErrorException):
    pass


class UnauthorizedException(UnrecoverableClientErrorException):
    pass


class PaymentRequiredException(UnrecoverableClientErrorException):
    pass


class ForbiddenException(UnrecoverableClientErrorException):
    pass


class NotFoundException(UnrecoverableClientErrorException):
    pass


class MethodNotAllowedException(UnrecoverableClientErrorException):
    pass


class NotAcceptableException(UnrecoverableClientErrorException):
    pass


class ProxyAuthenticationRequiredException(UnrecoverableClientErrorException):
    pass


class RequestTimeoutException(RecoverableClientErrorException):
    pass


class ConflictException(UnrecoverableClientErrorException):
    pass


class GoneException(UnrecoverableClientErrorException):
    pass


class LengthRequiredException(UnrecoverableClientErrorException):
    pass


class PreconditionFailedException(UnrecoverableClientErrorException):
    pass


class PayloadTooLargeException(UnrecoverableClientErrorException):
    pass


class URITooLongException(UnrecoverableClientErrorException):
    pass


class UnsupportedMediaTypeException(UnrecoverableClientErrorException):
    pass


class RangeNotSatisfiableException(UnrecoverableClientErrorException):
    pass


class ExpectationFailedException(UnrecoverableClientErrorException):
    pass


class IAmATeapotException(UnrecoverableClientErrorException):
    pass


class MisdirectedRequestException(UnrecoverableClientErrorException):
    pass


class UnprocessableEntityException(UnrecoverableClientErrorException):
    pass


class LockedException(UnrecoverableClientErrorException):
    pass


class FailedDependencyException(UnrecoverableClientErrorException):
    pass


class UpgradeRequiredException(UnrecoverableClientErrorException):
    pass


class UnavailableForLegalReasonsException(UnrecoverableClientErrorException):
    pass


class RequestHeaderFieldsTooLargeException(UnrecoverableClientErrorException):
    pass


class MethodFailureException(UnrecoverableClientErrorException):
    pass


class BlockedByWindowsParentalControlsException(UnrecoverableClientErrorException):
    pass


class InvalidTokenException(UnrecoverableClientErrorException):
    pass


class TokenRequiredException(UnrecoverableClientErrorException):
    pass


class RequestHasBeenForbiddenByAntivirusException(UnrecoverableClientErrorException):
    pass


class LoginTimeoutException(RecoverableClientErrorException):
    pass


class RetryWithException(RecoverableClientErrorException):
    pass


class SSLCertificateErrorException(UnrecoverableClientErrorException):
    pass


class SSLCertificateRequiredException(UnrecoverableClientErrorException):
    pass


class HTTPRequestSentToHTTPSPortException(UnrecoverableClientErrorException):
    pass


class NoResponseException(UnrecoverableClientErrorException):
    pass


class ClientClosedRequestException(RecoverableClientErrorException):
    pass


# HTTP Server Errors
# ==================

class ServerErrorException(HTTPError, RecoverableErrorMixin):
    pass


class InternalServerErrorException(ServerErrorException):
    pass


class NotImplementedException(ServerErrorException):
    pass


class BadGatewayException(ServerErrorException):
    pass


class ServiceUnavailableException(ServerErrorException):
    pass


class GatewayTimeoutException(ServerErrorException):
    pass


class HTTPVersionNotSupportedException(ServerErrorException):
    pass


class VariantAlsoNegotiatesException(ServerErrorException):
    pass


class InsufficientStorageException(ServerErrorException):
    pass


class LoopDetectedException(ServerErrorException):
    pass


class NotExtendedException(ServerErrorException):
    pass


class NetworkAuthenticationRequiredException(ServerErrorException):
    pass


class BandwidthLimitExceededException(ServerErrorException):
    pass


class SiteIsFrozenException(ServerErrorException):
    pass


class InvalidSSLCertificateException(ServerErrorException):
    pass


class SSLHandshakeFailedException(ServerErrorException):
    pass


class ATimeoutOccurredException(ServerErrorException):
    pass


class OriginIsUnreachableException(ServerErrorException):
    pass


class ConnectionTimedOutException(ServerErrorException):
    pass


class WebServerIsDownException(ServerErrorException):
    pass


class UnknownErrorException(ServerErrorException):
    pass
