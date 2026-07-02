from typing import Literal

import requests
from requests import Response

from py_canada_post.utils.error_handler import error_check
from py_canada_post.services.rating.types import Service
from py_canada_post.utils.response_to_object.serialization.get_service_to_object import GetServiceToObject


class GetService:
    def __init__(self, headers: dict, endpoint: str, customer_number: int, contract_id: int = None) -> None:
        """
        Initialize class variables.

        Parameters
        ----------
        headers : dict
            Headers passed to send in a request body.
        endpoint : str
            Endpoint to send a request to.
        customer_number : int
            Customer number that was obtained from Canada Post Developer Portal.
        contract_id : int, optional
            Contract id that was obtained from Canada Post Developer Portal.
        """

        self.headers = headers
        self.endpoint = endpoint
        self.customer_number = customer_number
        self.contract_id = contract_id

    def _construct_url(
        self,
        service_code: Literal[
           "DOM.RP",
           "DOM.EP",
           "DOM.XP",
           "DOM.XP.CERT",
           "DOM.PC",
           "DOM.LIB",
           "USA.EP",
           "USA.SP.AIR",
           "USA.TP",
           "USA.TP.LVM",
           "USA.XP",
           "INT.XP",
           "INT.IP.AIR",
           "INT.IP.SURF",
           "INT.SP.AIR",
           "INT.SP.SURF",
           "INT.TP"
        ],
        country_code: str = None
    ) -> str:
        """
        Function to generate url to get the service based on the service code, and,
        if provided, country code..

        Parameters
        ----------
        service_code : Literal[
           "DOM.RP",
           "DOM.EP",
           "DOM.XP",
           "DOM.XP.CERT",
           "DOM.PC",
           "DOM.LIB",
           "USA.EP",
           "USA.SP.AIR",
           "USA.TP",
           "USA.TP.LVM",
           "USA.XP",
           "INT.XP",
           "INT.IP.AIR",
           "INT.IP.SURF",
           "INT.SP.AIR",
           "INT.SP.SURF",
           "INT.TP"
        ]
            Service code.
        country_code : str, optional
            Country code in a 2-letter format (e.g. JP, CA, US).

        Returns
        -------
        str
            Constructed url.
        """

        endpoint = f"{self.endpoint}/rs/ship/service/{service_code}"

        if country_code:
            endpoint += "?" + country_code

        return endpoint

    def get_service(
        self,
        service_code: Literal[
           "DOM.RP",
           "DOM.EP",
           "DOM.XP",
           "DOM.XP.CERT",
           "DOM.PC",
           "DOM.LIB",
           "USA.EP",
           "USA.SP.AIR",
           "USA.TP",
           "USA.TP.LVM",
           "USA.XP",
           "INT.XP",
           "INT.IP.AIR",
           "INT.IP.SURF",
           "INT.SP.AIR",
           "INT.SP.SURF",
           "INT.TP"
        ],
        country_code: str = None
    ) -> Service | None:
        """
        Function to get service based on the service code and optionally,
        country code.

        Parameters
        ----------
        service_code : Literal[
           "DOM.RP",
           "DOM.EP",
           "DOM.XP",
           "DOM.XP.CERT",
           "DOM.PC",
           "DOM.LIB",
           "USA.EP",
           "USA.SP.AIR",
           "USA.TP",
           "USA.TP.LVM",
           "USA.XP",
           "INT.XP",
           "INT.IP.AIR",
           "INT.IP.SURF",
           "INT.SP.AIR",
           "INT.SP.SURF",
           "INT.TP"
        ]
            Service code.
        country_code : str, optional
            Country code in a 2-letter format (e.g. JP, CA, US).

        Returns
        -------
        Service or None
            Service or None.

        Examples
        --------
        >>> from py_canada_post.client import PyCanadaPost
        >>>
        >>> customer_number = 123456789
        >>> api_key = "your_api_key"
        >>> contract_id = 987654321
        >>>
        >>> py_canada_post = PyCanadaPost(
        >>>     customer_number=customer_number,
        >>>     api_key=api_key,
        >>>     contract_id=contract_id
        >>> )
        >>> service = py_canada_post.rating.get_service.get_service(
        >>>     service_code="DOM.RP"
        >>> )
        >>> print(service)
        """

        url = self._construct_url(service_code, country_code)
        response = requests.get(
            url=url,
            headers=self.headers,
        )

        error_check(response)
        return self.get_service_to_object(response)

    @staticmethod
    def get_service_to_object(response: Response) -> Service | None:
        """
        Function to transform Response type object into the readable and manageable dataclass format.

        Parameters
        ----------
        response : Response
            Response type object.

        Returns
        -------
        Service or None
            Service or None.
        """

        return GetServiceToObject(response).response_to_object()
