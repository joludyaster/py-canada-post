from xml.etree import ElementTree as ET
from datetime import datetime
from typing import Optional, Literal

import requests
from requests import Response

from .types import Destination, DomesticDestination, Option, ParcelCharacteristics, Rate
from ...utils.construct_xml_element import ConstructXMLElement
from ...utils.error_handler import error_handler
from ...utils.response_to_object.rate_to_object import RateToObject

construct = ConstructXMLElement()


class GetRates:

    def __init__(self, headers: dict, endpoint: str, customer_number: int, contract_id: Optional[int] = None):
        self.headers = headers
        self.endpoint = endpoint
        self.customer_number = customer_number
        self.contract_id = contract_id

    @error_handler
    def get_rates(
        self,
        origin_postal_code: str,
        destination: Destination,
        promo_code: Optional[str] = None,
        quote_type: Optional[Literal["commercial", "counter"]] = "commercial",
        expected_mailing_date: Optional[datetime] = None,
        options: Optional[list[Option]] = None,
        parcel_characteristics: Optional[ParcelCharacteristics] = None,
        unpackaged: bool = False,
        mailing_tube: bool = False,
        oversized: bool = False,
        services: Optional[list[Literal[
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
        ]]] = None
    ) -> Response:
        """
        Function to get rates for a shipping based on the provided arguments.

        Parameters
        ----------
        origin_postal_code : str
            Postal Code from which the parcel will be sent.
            Format ANANAN (only accepted with uppercase)
        destination : Destination
            Defines the destination of the parcel.
        promo_code : Optional[str], optional
            If you have a promotional discount code, enter it here. The discount amount will be returned in the response under the adjustment structure.
        quote_type : Optional[Literal["commercial", "counter"]], default "commercial"
            Either commercial or counter.

            - "commercial" will return the discounted price for the commercial customer or Solutions for Small Business member.
            - "counter" will return the regular price paid by consumers.
            Defaults to "commercial" if not specified.
        expected_mailing_date : Optional[datetime], optional
            The expected mailing date for the parcel.

            This date is used in calculations of the expected delivery date, however all rate quotes are based on the current system date.
        options : Optional[list[Option]], optional
            Structure containing the list of options desired for the shipment.
        parcel_characteristics : Optional[ParcelCharacteristics], optional
            Details of the parcel such as weight and dimensions.
        unpackaged : bool, default False
            Indicates that the parcel will be unpackaged (e.g. tires)
        mailing_tube : bool, default False
            Indicates that the object will be shipped in a mailing tube
        oversized : bool, default False
            Indicates that the object has oversized dimensions. Automatically set correctly if dimensions are provided.
        services : Optional[list[Literal[
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
        ]]], optional
            List of services to be used for the shipment.

        Returns
        -------
        Response
            Response object

        Examples
        --------
        >>> from core.client import PyCanadaPost

        >>> customer_number = 123456789
        >>> api_key = "your_api_key"
        >>> contract_id = 987654321

        >>> py_canada_post = PyCanadaPost(
        >>>    customer_number=customer_number,
        >>>    api_key=api_key,
        >>>    contract_id=contract_id
        >>> )

        >>> response = py_canada_post.rating.rates.get_rates(
        >>>    origin_postal_code="E4M8S3",
        >>>    destination=Destination(
        >>>        domestic=DomesticDestination(
        >>>            postal_code="T3Z1C8"
        >>>        )
        >>>    ),
        >>>    promo_code="YOUR_PROMO_CODE",
        >>>    quote_type="commercial",
        >>>    expected_mailing_date=datetime(2023, 10, 1),
        >>>    options=[Option(option_code="SO", option_amount=5.0)],
        >>>    parcel_characteristics=ParcelCharacteristics(
        >>>        weight=23.5
        >>>    ),
        >>>    unpackaged=True,
        >>>    mailing_tube=True,
        >>>    oversized=True,
        >>>    services=["DOM.RP"]
        >>> )
        >>> print(response.status_code)
        >>> print(response.text)
        """
        mailing_scenario = ET.Element("mailing-scenario", attrib={"xmlns": "http://www.canadapost.ca/ws/ship/rate-v4"})

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
            child_element = construct.construct_xml_element(
                parent_tag=tag,
                data=data,
                child_tag=child_tag[0] if child_tag else None
            )
            if child_element is not None:
                mailing_scenario.append(child_element)

        response = requests.post(
            url=f"{self.endpoint}/rs/ship/price",
            data=ET.tostring(mailing_scenario, encoding='utf-8'),
            headers=self.headers,
        )

        return response

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
    ) -> Optional[Rate]:
        """
        Function to get a rate based on the service provided

        Parameters
        ----------
        rates : list[Rate]
            List of rates available
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
            Service code to search for

        Returns
        -------
        Optional[Rate]
            Rate or None
        """
        for rate in rates:
            if rate.service.code == service_code:
                return rate

        return None


    @staticmethod
    def rate_to_object(response: Response) -> Optional[list[Rate]]:
        """
        Function to transform Response type object into the readable and manageable dataclass format

        Parameters
        ----------
        response : Response
            Response type object

        Returns
        -------
        Optional[list[Rate]]
            List of rate or None
        """
        return RateToObject(response=response).response_to_object()
