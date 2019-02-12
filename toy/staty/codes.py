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


from . import base
from . import exceptions
from .status_map import status


@status.register
class Continue(base.Informational, base.HTTP11Mixin):
    code = 100
    message = "Continue"
    rfcs = (
        ("7231", "6.2.1"),
    )


@status.register
class SwitchingProtocols(base.Informational, base.HTTP11Mixin):
    code = 101
    message = "Switching Protocols"
    rfcs = (
        ("7231", "6.2.2"),
    )


@status.register
class Processing(base.Informational, base.WebDAVMixin):
    code = 102
    message = "Processing"
    rfcs = (
        ("2518", ""),
    )


@status.register
class Checkpoint(base.Informational, base.UnofficialMixin):
    code = 103
    message = "Checkpoint"
    reference = "https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#Unofficial_codes"


@status.register
class Ok(base.Successful, base.HTTP10Mixin):
    code = 200
    message = "OK"
    rfcs = (
        ("7231", "6.3.1"),
    )


@status.register
class Created(base.Successful, base.HTTP10Mixin):
    code = 201
    message = "Created"
    rfcs = (
        ("7231", "6.3.2"),
    )


@status.register
class Accepted(base.Successful, base.HTTP10Mixin):
    code = 202
    message = "Accepted"
    rfcs = (
        ("7231", "6.3.3"),
    )


@status.register
class NonAuthoritativeInformation(base.Successful, base.HTTP11Mixin):
    code = 203
    message = "Non-Authoritative Information"
    rfcs = (
        ("7231", "6.3.4"),
    )


@status.register
class NoContent(base.Successful, base.HTTP10Mixin):
    code = 204
    message = "No Content"
    rfcs = (
        ("7231", "6.3.5"),
    )


@status.register
class ResetContent(base.Successful, base.HTTP11Mixin):
    code = 205
    message = "Reset Content"
    rfcs = (
        ("7231", "6.3.6"),
    )


@status.register
class PartialContent(base.Successful, base.HTTP11Mixin):
    code = 206
    message = "Partial Content"
    rfcs = (
        ("7233", "4.1"),
    )


@status.register
class MultiStatus(base.Successful, base.WebDAVMixin):
    code = 207
    message = "Multi-Status"
    rfcs = (
        ("4918", ""),
    )


@status.register
class AlreadyReported(base.Successful, base.WebDAVMixin):
    code = 208
    message = "Already Reported"
    rfcs = (
        ("5842", ""),
    )


@status.register
class IMUsed(base.Successful, base.HTTP11Mixin):
    code = 226
    message = "IM Used"
    rfcs = (
        ("3229", ""),
    )


@status.register
class MultipleChoices(base.Redirection, base.HTTP10Mixin):
    code = 300
    message = "Multiple Choices"
    rfcs = (
        ("7231", "6.4.1"),
    )


@status.register
class MovedPermanently(base.Redirection, base.HTTP10Mixin):
    code = 301
    message = "Moved Permanently"
    rfcs = (
        ("7231", "6.4.2"),
    )


@status.register
class Found(base.Redirection, base.HTTP11Mixin):
    code = 302
    message = "Found"
    rfcs = (
        ("7231", "6.4.3"),
    )


@status.register
class SeeOther(base.Redirection, base.HTTP11Mixin):
    code = 303
    message = "See Other"
    rfcs = (
        ("7231", "6.4.4"),
    )


@status.register
class NotModified(base.Redirection, base.HTTP11Mixin):
    code = 304
    message = "Not Modified"
    rfcs = (
        ("7232", "4.1"),
    )


@status.register
class UseProxy(base.Redirection, base.HTTP11Mixin):
    code = 305
    message = "Use Proxy"
    rfcs = (
        ("7231", "6.4.5"),
    )


@status.register
class SwitchProxy(base.Redirection, base.HTTP11Mixin):
    code = 306
    message = "Switch Proxy"  # Unused
    rfcs = (
        ("7231", "6.4.6"),
        ("draft", "1.2"),
    )


@status.register
class TemporaryRedirect(base.Redirection, base.HTTP11Mixin):
    code = 307
    message = "Temporary Redirect"
    rfcs = (
        ("7231", "6.4.7"),
    )


@status.register
class PermanentRedirect(base.Redirection, base.HTTP11Mixin):
    code = 308
    message = "Permanent Redirect"
    rfcs = (
        ("7538", ""),
    )


@status.register
class BadRequest(base.ClientError, base.HTTP10Mixin):
    code = 400
    message = "Bad Request"
    exception = exceptions.BadRequestException
    rfcs = (
        ("7231", "6.5.1"),
    )


@status.register
class Unauthorized(base.ClientError, base.HTTP10Mixin):
    code = 401
    message = "Unauthorized"
    exception = exceptions.UnauthorizedException
    rfcs = (
        ("7235", "3.1"),
    )


@status.register
class PaymentRequired(base.ClientError, base.HTTP10Mixin):
    code = 402
    message = "Payment Required"
    exception = exceptions.PaymentRequiredException
    rfcs = (
        ("7231", "6.5.2"),
    )


@status.register
class Forbidden(base.ClientError, base.HTTP10Mixin):
    code = 403
    message = "Forbidden"
    exception = exceptions.ForbiddenException
    rfcs = (
        ("7231", "6.5.3"),
    )


@status.register
class NotFound(base.ClientError, base.HTTP10Mixin):
    code = 404
    message = "Not Found"
    exception = exceptions.NotFoundException
    rfcs = (
        ("7231", "6.5.4"),
    )


@status.register
class MethodNotAllowed(base.ClientError, base.HTTP11Mixin):
    code = 405
    message = "Method Not Allowed"
    exception = exceptions.MethodNotAllowedException
    rfcs = (
        ("7231", "6.5.5"),
    )


@status.register
class NotAcceptable(base.ClientError, base.HTTP11Mixin):
    code = 406
    message = "Not Acceptable"
    exception = exceptions.NotAcceptableException
    rfcs = (
        ("7231", "6.5.6"),
    )


@status.register
class ProxyAuthenticationRequired(base.ClientError, base.HTTP11Mixin):
    code = 407
    message = "Proxy Authentication Required"
    exception = exceptions.ProxyAuthenticationRequiredException
    rfcs = (
        ("7235", "3.2"),
    )


@status.register
class RequestTimeout(base.ClientError, base.HTTP11Mixin):
    code = 408
    message = "Request Timeout"
    exception = exceptions.RequestTimeoutException
    rfcs = (
        ("7231", "6.5.7"),
    )


@status.register
class Conflict(base.ClientError, base.HTTP11Mixin):
    code = 409
    message = "Conflict"
    exception = exceptions.ConflictException
    rfcs = (
        ("7231", "6.5.8"),
    )


@status.register
class Gone(base.ClientError, base.HTTP11Mixin):
    code = 410
    message = "Gone"
    exception = exceptions.GoneException
    rfcs = (
        ("7231", "6.5.9"),
    )


@status.register
class LengthRequired(base.ClientError, base.HTTP11Mixin):
    code = 411
    message = "Length Required"
    exception = exceptions.LengthRequiredException
    rfcs = (
        ("7231", "6.5.10"),
    )


@status.register
class PreconditionFailed(base.ClientError, base.HTTP11Mixin):
    code = 412
    message = "Precondition Failed"
    exception = exceptions.PreconditionFailedException
    rfcs = (
        ("7232", "4.2"),
        ("8144", "3.2"),
    )


@status.register
class PayloadTooLarge(base.ClientError, base.HTTP11Mixin):
    code = 413
    message = "Payload Too Large"
    exception = exceptions.PayloadTooLargeException
    rfcs = (
        ("7231", "6.5.11"),
    )


@status.register
class URITooLong(base.ClientError, base.HTTP11Mixin):
    code = 414
    message = "URI Too Long"
    exception = exceptions.URITooLongException
    rfcs = (
        ("7231", "6.5.12"),
    )


@status.register
class UnsupportedMediaType(base.ClientError, base.HTTP11Mixin):
    code = 415
    message = "Unsupported Media Type"
    exception = exceptions.UnsupportedMediaTypeException
    rfcs = (
        ("7231", "6.5.13"),
        ("7694", "3"),
    )


@status.register
class RangeNotSatisfiable(base.ClientError, base.HTTP11Mixin):
    code = 416
    message = "Range Not Satisfiable"
    exception = exceptions.RangeNotSatisfiableException
    rfcs = (
        ("7233", "4.4"),
    )


@status.register
class ExpectationFailed(base.ClientError, base.HTTP11Mixin):
    code = 417
    message = "Expectation Failed"
    exception = exceptions.ExpectationFailedException
    rfcs = (
        ("7231", "6.5.14"),
    )


@status.register
class IAmATeapot(base.ClientError, base.HTCPCP10Mixin):
    code = 418
    message = "I am a teapot"
    exception = exceptions.IAmATeapotException


@status.register
class MethodFailure(base.ClientError, base.UnofficialMixin):
    code = 420
    message = "Method Failure"
    exception = exceptions.MethodFailureException
    reference = "Spring Framework"


@status.register
class MisdirectedRequest(base.ClientError, base.HTTP20Mixin):
    code = 421
    message = "Misdirected Request"
    exception = exceptions.MisdirectedRequestException
    rfcs = (
        ("7540", "9.1.2"),
    )


@status.register
class UnprocessableEntity(base.ClientError, base.WebDAVMixin):
    code = 422
    message = "Unprocessable Entity"
    exception = exceptions.UnprocessableEntityException
    rfcs = (
        ("4918", ""),
    )


@status.register
class Locked(base.ClientError, base.WebDAVMixin):
    code = 423
    message = "Locked"
    exception = exceptions.LockedException
    rfcs = (
        ("4918", ""),
    )


@status.register
class FailedDependency(base.ClientError, base.WebDAVMixin):
    code = 424
    message = "Failed Dependency"
    exception = exceptions.FailedDependencyException
    rfcs = (
        ("4918", ""),
    )


@status.register
class UpgradeRequired(base.ClientError, base.HTTP11Mixin):
    code = 426
    message = "Upgrade Required"
    exception = exceptions.UpgradeRequiredException
    rfcs = (
        ("7231", "6.5.15"),
    )


@status.register
class PreconditionRequired(base.ClientError, base.HTTP11Mixin):
    code = 428
    message = "Precondition Required"
    exception = exceptions.PreconditionRequiredException
    rfcs = (
        ("6585", ""),
    )


@status.register
class TooManyRequests(base.ClientError, base.HTTP11Mixin):
    code = 429
    message = "Too Many Requests"
    exception = exceptions.TooManyRequestsException
    rfcs = (
        ("6585", ""),
    )


@status.register
class RequestHeaderFieldsTooLarge(base.ClientError, base.HTTP11Mixin):
    code = 431
    message = "Request Header Fields Too Large"
    exception = exceptions.RequestHeaderFieldsTooLargeException
    rfcs = (
        ("6585", ""),
    )


@status.register
class LoginTimeout(base.ClientError, base.IISMixin):
    code = 440
    message = "Login Timeout"
    exception = exceptions.LoginTimeoutException


@status.register
class NoResponse(base.ClientError, base.NginxMixin):
    code = 444
    message = "No Response"
    exception = exceptions.NoResponseException


@status.register
class RetryWith(base.ClientError, base.IISMixin):
    code = 449
    message = "Retry With"
    exception = exceptions.RetryWithException


@status.register
class BlockedByWindowsParentalControls(base.ClientError, base.UnofficialMixin):
    code = 450
    message = "Blocked By Windows Parental Controls"
    reference = "Microsoft"
    exception = exceptions.BlockedByWindowsParentalControlsException


@status.register
class UnavailableForLegalReasons(base.ClientError, base.HTTP11Mixin):
    code = 451
    message = "Unavailable For Legal Reasons"
    exception = exceptions.UnavailableForLegalReasonsException
    rfcs = (
        ("7725", ""),
    )


class Redirect(base.ClientError, base.IISMixin):
    code = 451
    message = "Redirect"
    exception = exceptions.BadGatewayException


@status.register
class SSLCertificateError(base.ClientError, base.NginxMixin):
    code = 495
    message = "SSL Certificate Error"
    exception = exceptions.SSLCertificateErrorException


@status.register
class SSLCertificateRequired(base.ClientError, base.NginxMixin):
    code = 496
    message = "SSL Certificate Required"
    exception = exceptions.SSLCertificateRequiredException


@status.register
class HTTPRequestSentToHTTPSPort(base.ClientError, base.NginxMixin):
    code = 497
    message = "HTTP Request Sent To HTTPS Port"
    exception = exceptions.HTTPRequestSentToHTTPSPortException


@status.register
class InvalidToken(base.ClientError, base.UnofficialMixin):
    code = 498
    message = "Invalid Token"
    reference = "ArcGIS for Server"
    exception = exceptions.InvalidTokenException


@status.register
class ClientClosedRequest(base.ClientError, base.NginxMixin):
    code = 499
    message = "Client Closed Request"
    exception = exceptions.ClientClosedRequestException


class RequestHasBeenForbiddenByAntivirus(base.ClientError, base.UnofficialMixin):
    code = 499
    message = "Request Has Been Forbidden By Antivirus"
    reference = "https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#Unofficial_codes"
    exception = exceptions.RequestHasBeenForbiddenByAntivirusException


class TokenRequired(base.ClientError, base.UnofficialMixin):
    code = 499
    message = "Token Required"
    reference = "ArcGIS for Server"
    exception = exceptions.TokenRequiredException


@status.register
class InternalServerError(base.ServerError, base.HTTP10Mixin):
    code = 500
    message = "Internal Server Error"
    exception = exceptions.InternalServerErrorException
    rfcs = (
        ("7231", "6.6.1"),
    )


# noinspection PyShadowingBuiltins
@status.register
class NotImplemented(base.ServerError, base.HTTP10Mixin):
    code = 501
    message = "Not Implemented"
    exception = exceptions.NotImplementedException
    rfcs = (
        ("7231", "6.6.2"),
    )


@status.register
class BadGateway(base.ServerError, base.HTTP10Mixin):
    code = 502
    message = "Bad Gateway"
    exception = exceptions.BadGatewayException
    rfcs = (
        ("7231", "6.6.3"),
    )


@status.register
class ServiceUnavailable(base.ServerError, base.HTTP10Mixin):
    code = 503
    message = "Service Unavailable"
    exception = exceptions.ServiceUnavailableException
    rfcs = (
        ("7231", "6.6.4"),
    )


@status.register
class GatewayTimeout(base.ServerError, base.HTTP11Mixin):
    code = 504
    message = "Gateway Timeout"
    exception = exceptions.GatewayTimeoutException
    rfcs = (
        ("7231", "6.6.5"),
    )


@status.register
class HTTPVersionNotSupported(base.ServerError, base.HTTP11Mixin):
    code = 505
    message = "HTTP Version Not Supported"
    exception = exceptions.HTTPVersionNotSupportedException
    rfcs = (
        ("7231", "6.6.6"),
    )


@status.register
class VariantAlsoNegotiates(base.ServerError, base.HTTP11Mixin):
    code = 506
    message = "Variant Also Negotiates"
    exception = exceptions.VariantAlsoNegotiatesException
    rfcs = (
        ("2295", ""),
    )


@status.register
class InsufficientStorage(base.ServerError, base.WebDAVMixin):
    code = 507
    message = "Insufficient Storage"
    exception = exceptions.InsufficientStorageException
    rfcs = (
        ("4918", ""),
    )


@status.register
class LoopDetected(base.ServerError, base.WebDAVMixin):
    code = 508
    message = "Loop Detected"
    exception = exceptions.LoopDetectedException
    rfcs = (
        ("5842", ""),
    )


class BandwidthLimitExceeded(base.ServerError, base.UnofficialMixin):
    code = 509
    message = "Bandwidth Limit Exceeded"
    reference = "Apache Web Server/cPanel"
    exception = exceptions.BandwidthLimitExceededException


@status.register
class NotExtended(base.ServerError, base.HTTP11Mixin):
    code = 510
    message = "Not Extended"
    exception = exceptions.NotExtendedException
    rfcs = (
        ("2774", ""),
    )


@status.register
class NetworkAuthenticationRequired(base.ServerError, base.HTTP11Mixin):
    code = 511
    message = "Network Authentication Required"
    exception = exceptions.NetworkAuthenticationRequiredException
    rfcs = (
        ("6585", ""),
    )


@status.register
class UnknownError(base.ServerError, base.CloudflareMixin):
    code = 520
    message = "Unknown Error"
    exception = exceptions.UnknownErrorException


@status.register
class WebServerIsDown(base.ServerError, base.CloudflareMixin):
    code = 521
    message = "Web Server Is Down"
    exception = exceptions.WebServerIsDownException


@status.register
class ConnectionTimedOut(base.ServerError, base.CloudflareMixin):
    code = 522
    message = "Connection Timed Out"
    exception = exceptions.ConnectionTimedOutException


@status.register
class OriginIsUnreachable(base.ServerError, base.CloudflareMixin):
    code = 523
    message = "Origin Is Unreachable"
    exception = exceptions.OriginIsUnreachableException


@status.register
class ATimeoutOccurred(base.ServerError, base.CloudflareMixin):
    code = 524
    message = "A Timeout Occurred"
    exception = exceptions.ATimeoutOccurredException


@status.register
class SSLHandshakeFailed(base.ServerError, base.CloudflareMixin):
    code = 525
    message = "SSL Handshake Failed"
    exception = exceptions.SSLHandshakeFailedException


@status.register
class InvalidSSLCertificate(base.ServerError, base.CloudflareMixin):
    code = 526
    message = "Invalid SSL Certificate"
    exception = exceptions.InvalidSSLCertificateException


@status.register
class SiteIsFrozen(base.ServerError, base.UnofficialMixin):
    code = 530
    message = "Site Is Frozen"
    reference = "Pantheon"
    exception = exceptions.SiteIsFrozenException
