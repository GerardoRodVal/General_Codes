
class RequestError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_message = ""
        self.error_code = None
        self.status_code = None

    def serialize(self, include_error_code=False, include_status_code=True):
        response = {
            "error_message": self.error_message,
        }
        if include_status_code:
            response["status_code"] = self.status_code
        if include_error_code:
            response["error_code"] = self.error_code
        return response


class BadRequestError(RequestError):
    """
    The server cannot or will not process the request
    due to an apparent client error.
    """

    def __init__(
            self,
            error_message="Bad request.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 400


class UnauthorizedError(RequestError):
    """
    Authentication is required and has failed or has not yet been provided.
    """

    def __init__(
            self,
            error_message="Unauthorized request.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 401


class PaymentRequiredError(RequestError):
    """
    Reserved for future use.
    The original intention was that this code might be used as
    part of some form of digital cash or micropayment scheme,
    as proposed, for example, by GNU Taler,[34] but that has not
    yet happened, and this code is not widely used.
    """

    def __init__(
            self,
            error_message="Payment required.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 402


class ForbiddenError(RequestError):
    """
    The request contained valid data and was understood by
    the server, but the server is refusing the action.
    """

    def __init__(
            self,
            error_message="Forbidden request.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 403


class NotFoundError(RequestError):
    """
    The requested resource could not be found
    but may be available in the future.
    """

    def __init__(
            self,
            error_message="Resource not found.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 404


class MethodNotAllowedError(RequestError):
    """
    Request method is not supported for the requested resource.
    """

    def __init__(
            self,
            error_message="Method not allowed.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 405


class NotAcceptableError(RequestError):
    """
    The requested resource is capable of generating only content not
    acceptable according to the Accept headers sent in the request.
    """

    def __init__(
            self,
            error_message="Not acceptable request.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 406


class ProxyAuthenticationRequiredError(RequestError):
    """
    The client must first authenticate itself with the proxy.
    """

    def __init__(
            self,
            error_message="Proxy Authentication Required.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 407


class TimeOutError(RequestError):
    """
    The server timed out waiting for the request.
    """

    def __init__(
            self,
            error_message="Timeout.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 408


class ConflictError(RequestError):
    """
    Indicates that the request could not be processed because of
    conflicts in the current state of the resource.
    """

    def __init__(
            self,
            error_message="Conflict.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 409


class GoneError(RequestError):
    """
    Indicates that the resource requested is no longer available and
    will not be available again..
    """

    def __init__(
            self,
            error_message="Gone.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 410


class LengthRequiredError(RequestError):
    """
    The request did not specify the length of its content,
    which is required by the requested resource.
    """

    def __init__(
            self,
            error_message="Length required.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 411


class PreconditionFailedError(RequestError):
    """
    The server does not meet one of the preconditions that the
    requester put on the request header fields.
    """

    def __init__(
            self,
            error_message="Precondition Failed.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 412


class PayloadTooLargeError(RequestError):
    """
    The request is larger than the server is willing or able to process.
    """

    def __init__(
            self,
            error_message="Payload Too Large.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 413


class URITooLongError(RequestError):
    """
    The URI provided was too long for the server to process.
    """

    def __init__(
            self,
            error_message="URI Too Long.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 414


class UnsupportedMediaTypeError(RequestError):
    """
    The request entity has a media type which the server
    or resource does not support.
    """

    def __init__(
            self,
            error_message="Unsupported Media Type.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 415


class RangeNotSatisfiableeError(RequestError):
    """
    The client has asked for a portion of the file
    (byte serving), but the server cannot supply that portion.
    """

    def __init__(
            self,
            error_message="Range Not Satisfiablee.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 416


class ExpectationFailedError(RequestError):
    """
    The server cannot meet the requirements of the Expect request-header field.
    """

    def __init__(
            self,
            error_message="Expectation Failed.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 417


class MisdirectedRequestError(RequestError):
    """
    The request was directed at a server that is not able to
    produce a response.
    """

    def __init__(
            self,
            error_message="Misdirected Request.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 421


class UnprocessableEntityError(RequestError):
    """
    The request was well-formed but was unable to be
    followed due to semantic errors.
    """

    def __init__(
            self,
            error_message="UnprocessableEntity.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 422


class LockedError(RequestError):
    """
    The resource that is being accessed is locked.
    """

    def __init__(
            self,
            error_message="Locked.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 423


class FailedDependencyError(RequestError):
    """
    The request failed because it depended on
    another request and that request failed.
    """

    def __init__(
            self,
            error_message="Failed Dependency.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 424


class TooEarlyError(RequestError):
    """
    Indicates that the server is unwilling
    to risk processing a request that might be replayed.
    """

    def __init__(
            self,
            error_message="Too Early.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 425


class UpgradeRequiredError(RequestError):
    """
    Indicates that the server is unwilling
    to risk processing a request that might be replayed.
    """

    def __init__(
            self,
            error_message="Upgrade Required.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 426


class PreconditionRequiredError(RequestError):
    """
    The origin server requires the request to be conditional.
    """

    def __init__(
            self,
            error_message="Precondition Required.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 428


class TooManyRequestsError(RequestError):
    """
    The user has sent too many requests in a given amount of time.
    """

    def __init__(
            self,
            error_message="Too Many Requests.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 429


class RequestHeaderFieldsTooLargeError(RequestError):
    """
    The server is unwilling to process the request
    because either an individual header field, or
    all the header fields collectively, are too large.
    """

    def __init__(
            self,
            error_message="Request Header Fields Too Large.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 431


class UnavailableForLegalReasonsError(RequestError):
    """
    A server operator has received a legal demand to deny
    access to a resource or to a set of resources that
    includes the requested resource.
    """

    def __init__(
            self,
            error_message="Unavailable For Legal Reasons.",
            error_code=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.error_message = error_message
        self.error_code = error_code
        self.status_code = 451
