class CanadaPostError(Exception):
    def __init__(self, description: str, mitigation: str = None, status_code: int | str = None) -> None:
        """
        Initialize class variables.

        Parameters
        ----------
        description : str
            Description of the error to display.
        mitigation : str, optional
            Steps to fix the issue arisen.
        status_code : int or str, optional
            Status code of the error.
        """

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


# ========================
# EXCEPTIONS FOR "DISCOVER
# SERVICES" SECTION
# ========================
class InvalidContractNumber(CanadaPostError):
    """
    Error code: 2550
    """

    pass


class InvalidPostalCode(CanadaPostError):
    """
    Error code: 7266
    """

    pass


class InvalidDestinationCountry(CanadaPostError):
    """
    Error code: 8534
    """

    pass


class MissingOriginPostalCode(CanadaPostError):
    """
    Error code: 9194
    """

    pass
