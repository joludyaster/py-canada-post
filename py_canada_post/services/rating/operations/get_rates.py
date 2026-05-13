from datetime import datetime
from typing import Literal
from xml.etree import ElementTree as ET

import requests
from requests import Response

from py_canada_post.services.rating.types import Destination, Option, ParcelCharacteristics, Rate
from py_canada_post.utils.construct_xml_element import ConstructXMLElement
from py_canada_post.utils.error_handler import error_check
from py_canada_post.utils.response_to_object.serialization.rate_to_object import RateToObject

construct = ConstructXMLElement()


class GetRates:
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

    def get_rates(
            self,
            origin_postal_code: str,
            destination: Destination,
            promo_code: str = None,
            quote_type: Literal["commercial", "counter"] = "commercial",
            expected_mailing_date: datetime = None,
            options: list[Option] = None,
            parcel_characteristics: ParcelCharacteristics = None,
            unpackaged: bool = False,
            mailing_tube: bool = False,
            oversized: bool = False,
            services: list[Literal[
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
            ]] = None
    ) -> list[Rate] | None:
        """
        Function to get rates for a shipping based on the provided arguments.

        Parameters
        ----------
        origin_postal_code : str
            Postal Code from which the parcel will be sent.
            Format ANANAN (only accepted with uppercase)
        destination : Destination
            Defines the destination of the parcel.
        promo_code : str, optional
            If you have a promotional discount code, enter it here.
            The discount amount will be returned in the response under the adjustment structure.
        quote_type : Literal["commercial", "counter"], default "commercial"
            Either commercial or counter.

            - "commercial" will return the discounted price for the commercial customer or Solutions for Small Business member.
            - "counter" will return the regular price paid by consumers.
            Defaults to "commercial" if not specified.
        expected_mailing_date : datetime, optional
            The expected mailing date for the parcel.

            This date is used in calculations of the expected delivery date,
            however all rate quotes are based on the current system date.
        options : list[Option], optional
            Structure containing the list of options desired for the shipment.
        parcel_characteristics : ParcelCharacteristics, optional
            Details of the parcel such as weight and dimensions.
        unpackaged : bool, default False
            Indicates that the parcel will be unpackaged (e.g. tires).
        mailing_tube : bool, default False
            Indicates that the object will be shipped in a mailing tube.
        oversized : bool, default False
            Indicates that the object has oversized dimensions. Automatically set correctly if dimensions are provided.
        services : list[Literal["DOM.RP", "DOM.EP", "DOM.XP", "DOM.XP.CERT", "DOM.PC", "DOM.LIB", "USA.EP", "USA.SP.AIR", "USA.TP", "USA.TP.LVM", "USA.XP", "INT.XP", "INT.IP.AIR", "INT.IP.SURF", "INT.SP.AIR", "INT.SP.SURF", "INT.TP"]], optional
            List of services to be used for the shipment.

        Returns
        -------
        list[Rate] or None
            List of rates or None.

        Examples
        --------
        >>> from py_canada_post.client import PyCanadaPost
        >>> from py_canada_post.services.rating.types import Destination, DomesticDestination, Option, ParcelCharacteristics
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
        >>>
        >>> rates = py_canada_post.rating.rates.get_rates(
        >>>     origin_postal_code="E4M8S3",
        >>>     destination=Destination(
        >>>         domestic=DomesticDestination(
        >>>             postal_code="T3Z1C8"
        >>>         )
        >>>     ),
        >>>     promo_code="YOUR_PROMO_CODE",
        >>>     quote_type="commercial",
        >>>     expected_mailing_date=datetime(2023, 10, 1),
        >>>     options=[Option(option_code="SO", option_amount=5.0)],
        >>>     parcel_characteristics=ParcelCharacteristics(
        >>>         weight=23.5
        >>>     ),
        >>>     unpackaged=True,
        >>>     mailing_tube=True,
        >>>     oversized=True,
        >>>     services=["DOM.RP"]
        >>> )
        >>> print(rates)
        """

        mailing_scenario = ET.Element("mailing-scenario", {"xmlns": "http://www.canadapost.ca/ws/ship/rate-v4"})

        for item in [
            ("origin-postal-code", origin_postal_code),
            ("customer-number", self.customer_number),
            ("contract-id", self.contract_id),
            ("promo-code", promo_code),
            ("quote-type", quote_type),
            ("expected-mailing-date", expected_mailing_date),
            ("unpackaged", unpackaged),
            ("mailing-tube", mailing_tube),
            ("oversized", oversized),
            ("destination", destination),
            ("parcel-characteristics", parcel_characteristics),
            ("services", services, "service-code"),
            ("options", options, "option")
        ]:
            tag, data, *child_tag = item
            child_element = construct.construct_xml_element(tag, data, child_tag[0] if child_tag else None)
            if child_element is not None:
                mailing_scenario.append(child_element)

        response = requests.post(
            url=f"{self.endpoint}/rs/ship/price",
            data=ET.tostring(mailing_scenario, encoding='utf-8'),
            headers=self.headers,
        )

        error_check(response)
        return self.rate_to_object(response)

    @staticmethod
    def get_rate_by_service(
            rates: list[Rate],
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
            ]
    ) -> Rate | None:
        """
        Function to get a rate based on the service provided.

        Parameters
        ----------
        rates : list[Rate]
            List of rates available.
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
            Service code to search for.

        Returns
        -------
        Rate or None
            Rate or None.
        """

        for rate in rates:
            if rate.service.code == service_code:
                return rate

        return None

    @staticmethod
    def rate_to_object(response: Response) -> list[Rate] | None:
        """
        Function to transform Response type object into the readable and manageable dataclass format.

        Parameters
        ----------
        response : Response
            Response type object.

        Returns
        -------
        list[Rate] or None
            List of rates or None.
        """

        return RateToObject(response).response_to_object()
