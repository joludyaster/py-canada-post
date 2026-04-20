from typing import Optional, Any

import requests
from requests import Response

from core.services.rating.types import Service
from core.utils.error_handler import error_handler
from core.utils.response_to_object.service_to_object import ServiceToObject


class DiscoverServices:

    def __init__(self, headers: dict, endpoint: str, customer_number: int, contract_id: Optional[int] = None) -> None:
        self.headers = headers
        self.endpoint = endpoint
        self.customer_number = customer_number
        self.contract_id = contract_id

    def _construct_url(self, country_code: str, origin_postal_code: Optional[str] = None, destination_postal_code: Optional[str] = None) -> str:
        """
        Function to generate url to get the services based on the country code, origin postal code, destination postal code and contract number

        Parameters
        ----------
        country_code : str
            Country code in a 2-letter format (e.g. JP, CA, US)
        origin_postal_code : Optional[str], optional
            Origin postal code where the package will be sent from
        destination_postal_code : Optional[str], optional
            Destination postal code where the package will be delivered to

        Returns
        -------
        str
            Constructed url
        """
        endpoint = f"{self.endpoint}/rs/ship/service?"

        for key, value in {
            "country": country_code,
            "contract": self.contract_id,
            "origpc": origin_postal_code,
            "destpc": destination_postal_code
        }.items():
            if value is not None:
                endpoint += f"&{key}={value}"

        return endpoint

    @error_handler
    def discover_services(self, country_code: str, origin_postal_code: Optional[str] = None, destination_postal_code: Optional[str] = None) -> Any:
        """
        Function to discover services based on the country code, origin postal code, destination postal code and contract number

        Parameters
        ----------
        country_code : str
            Country code in a 2-letter format (e.g. JP, CA, US)
        origin_postal_code : Optional[str], optional
            Origin postal code where the package will be sent from
        destination_postal_code : Optional[str], optional
            Destination postal code where the package will be delivered to

        Returns
        -------
        Any
            Response object
        """
        url = self._construct_url(
            country_code=country_code,
            origin_postal_code=origin_postal_code,
            destination_postal_code=destination_postal_code
        )
        response = requests.get(
            url=url,
            headers=self.headers,
        )

        return response

    @staticmethod
    def service_to_object(response: Response) -> Optional[list[Service]]:
        """
        Function to transform a response object into the readable and manageable dataclass format

        Parameters
        ----------
        response : Response
            Response type object

        Returns
        -------
        Optional[list[Service]]
            List of services or None
        """
        return ServiceToObject(response=response).response_to_object()