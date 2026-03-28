from typing import Optional, Union


class CanadaPostError(BaseException):
    def __init__(self, description: str, mitigation: Optional[str] = None, status_code: Optional[Union[int, str]] = None):
        self.description = description
        self.mitigation = mitigation
        self.status_code = status_code
        super().__init__(". ".join(filter(None, [self.description, self.mitigation])))


class ServerError(CanadaPostError):
    """
    Error code: Server
    """
    pass


class UserIdDeactivated(CanadaPostError):
    """
    Error code: AA001
    """
    pass


class EndpointMissmatch(CanadaPostError):
    """
    Error code: AA002
    """
    pass


class APIMissmatch(CanadaPostError):
    """
    Error code: AA003
    """
    pass


class InvalidCustomer(CanadaPostError):
    """
    Error code: AA004
    """
    pass


class UnspecifiedPlatform(CanadaPostError):
    """
    Error code: AA005
    """
    pass


class PlatformNotAuthorized(CanadaPostError):
    """
    Error code: AA006
    """
    pass



class InactivePlatform(CanadaPostError):
    """
    Error code: AA007
    """
    pass



class UnauthorizedPlatform(CanadaPostError):
    """
    Error code: AA008
    """
    pass

class InvalidPlatformKeyType(CanadaPostError):
    """
    Error code: AA009
    """
    pass


class IncorrectPlatformRequest(CanadaPostError):
    """
    Error code: AA010
    """
    pass

class PostOfficesNotFound(CanadaPostError):
    """
    Error code: E00010
    """
    pass
