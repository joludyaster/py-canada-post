from requests import Response
from py_canada_post.services.rating.types import Service
from py_canada_post.utils.response_to_object.serialization.rate_to_object import ResponseToObject

SERVICES = "services"
SERVICE = "service"

SERVICE_NAME = "service-name"
SERVICE_CODE = "service-code"
SERVICE_LINK = "link"
HREF = "@href"

class ServiceToObject(ResponseToObject):
    def __init__(self, response: Response):
        super().__init__(response)

    def response_to_object(self):
        return self._construct_services(self.parsed_response)

    def _construct_services(self, obj: dict) -> list[Service] | None:
        return self._construct_objects(
            obj,
            [SERVICES, SERVICE],
            [SERVICE_CODE, SERVICE_NAME, (SERVICE_LINK, HREF)],
            Service
        )
