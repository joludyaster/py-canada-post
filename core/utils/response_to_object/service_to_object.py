from typing import Optional
from requests import Response

from ...services.rating.types import Service
from ..response_to_object import ResponseToObject

SERVICES = "services"
SERVICE = "service"

SERVICE_NAME = "service-name"
SERVICE_CODE = "service-code"
SERVICE_LINK = "link"
HREF = "@href"

class ServiceToObject(ResponseToObject):
    def __init__(self, response: Response):
        super().__init__(response=response)

    def response_to_object(self):
        return self._construct_services(obj=self.parsed_response)

    def _construct_services(self, obj: dict) -> Optional[list[Service]]:
        return self._construct_objects(
            obj=obj,
            search_keys=[SERVICES, SERVICE],
            obj_keys=[SERVICE_CODE, SERVICE_NAME, (SERVICE_LINK, HREF)],
            cls=Service
        )
