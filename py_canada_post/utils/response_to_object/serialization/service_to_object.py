from requests import Response

from py_canada_post.services.rating.types import Service
from py_canada_post.utils.response_to_object.serialization.rate_to_object import ResponseToObject

SERVICES = "services"
SERVICE = "service"

SERVICE_NAME = "service-name"
SERVICE_CODE = "service-code"


class ServiceToObject(ResponseToObject):
    def __init__(self, response: Response) -> None:
        """
        Initialize class variables.

        Parameters
        ----------
        response : Response
            Response object.
        """

        super().__init__(response)

    def response_to_object(self) -> list[Service] | None:
        """
        Main function to deserialize xml response object.

        Returns
        -------
        list[Service] or None
            List of services or None.
        """

        return self._construct_services(self.parsed_response)

    def _construct_services(self, obj: dict) -> list[Service] | None:
        """
        Function to construct services.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        list[Service] or None
            List of services or None
        """

        return self._construct_objects(
            obj,
            [SERVICES, SERVICE],
            [SERVICE_CODE, SERVICE_NAME],
            Service
        )
