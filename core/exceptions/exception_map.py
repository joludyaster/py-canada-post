from typing import Optional

from .exceptions import ServerError, UserIdDeactivated, EndpointMissmatch, APIMissmatch, InvalidCustomer, \
    UnspecifiedPlatform, PlatformNotAuthorized, InactivePlatform, UnauthorizedPlatform, InvalidPlatformKeyType, \
    IncorrectPlatformRequest, PostOfficesNotFound


class ExceptionDefinition:
    def __init__(self, exception: type[BaseException], description: str, mitigation: Optional[str] = None):
        self.exception = exception
        self.description = description
        self.mitigation = mitigation

ERROR_MAP = {
    "Server": ExceptionDefinition(
        ServerError,
        "Rejected by SLM Monitor",
        "You have exceeded the throttle limit for your API key. You will be blocked from making additional calls for up to a minute."
    ),
    "AA001": ExceptionDefinition(
        UserIdDeactivated,
        "The user id for the request has been deactivated. If you withdrew from the Developer Program, rejoin the program.",
        "From the Developer Program website, select Join Now."
    ),
    "AA002": ExceptionDefinition(
        EndpointMissmatch,
        "The username and password of the request do not match the endpoint. E.g. development key against production endpoint or vice versa.",
        "Merchant requests cannot be sent to the development environment."
    ),
    "AA003": ExceptionDefinition(
        APIMissmatch,
        "The API key in the 'Authorization' header does not match the mailed-by customer number in the request.",
        "Verify your data."
    ),
    "AA004": ExceptionDefinition(
        InvalidCustomer,
        "You cannot mail on behalf of the requested customer."
    ),
    "AA005": ExceptionDefinition(
        UnspecifiedPlatform,
        "Platform id not specified",
        "The platform-id header variable is empty or not present in the URL. This should only be encountered during platform development coding."
    ),
    "AA006": ExceptionDefinition(
        PlatformNotAuthorized,
        "Platform not authorized",
        """
The platform-id specified is incorrect or the merchant subsequently came to Canada Post and intentionally revoked permission for your platform to submit transactions on its behalf. The merchant could be asked to revalidate with Canada Post if they want to re-establish their relationship with the platform.

This error would also occur if the online owner of the platform key voluntarily withdrew from the Developer Program.

In rare cases, Canada Post may have deactivated the entire platform status due to fraud or misuse concerns.
        """
    ),
    "AA007": ExceptionDefinition(
        InactivePlatform,
        "Platform not active",
        """
You will receive this error if you have tried to use Get Merchant Registration Token while your application to become an approved e-commerce platform with Canada Post is still pending. You cannot use this service until Canada Post has approved your application.

In rare cases, Canada Post may have deactivated the entire platform status due to fraud or misuse concerns.
        """
    ),
    "AA008": ExceptionDefinition(
        UnauthorizedPlatform,
        "Unauthorized Platform",
        "You will receive this error if you are attempting to use Get Merchant Registration Token service but have not applied to become an e-commerce platform with Canada Post. To apply, sign in to the Developer Program home page and select Become a Platform."
    ),
    "AA009": ExceptionDefinition(
        InvalidPlatformKeyType,
        "Key type not valid for platform-id",
        "If a key other than a merchant key is being used to authenticate a transaction, the platform-id field must not be specified. Remove the platform-id field from the request even if you are a registered platform. Only requests done on behalf of a merchant can specify the platform-id."
    ),
    "AA010": ExceptionDefinition(
        IncorrectPlatformRequest,
        "Incorrectly configured platform request.",
        "The platform-id in the header and the platform-id in the URL disagree. These values must match."
    ),
    "E00010": ExceptionDefinition(
        PostOfficesNotFound,
        "No Post Offices found"
    )
}