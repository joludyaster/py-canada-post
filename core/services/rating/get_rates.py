from xml.etree import ElementTree as ET
from datetime import datetime
from typing import Optional, Literal

import requests
from requests import Response

from .types import Destination, DomesticDestination, Option, ParcelCharacteristics, Rates, Rate
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

    def _get_headers(self) -> dict:
        headers = self.headers.copy()
        headers.update(
            {
                "Accept": "application/vnd.cpc.ship.rate-v4+xml",
                "Content-Type": "application/vnd.cpc.ship.rate-v4+xml"
            }
        )
        return headers

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
    ) -> Response:
        """
        Function to get rates for a shipping based on the provided arguments.

        Parameters
        ----------
        origin_postal_code
            Postal Code from which the parcel will be sent.
            Format ANANAN (only accepted with uppercase)
        destination
            Defines the destination of the parcel.
        promo_code
            If you have a promotional discount code, enter it here. The discount amount will be returned in the response under the adjustment structure.
        quote_type
            Either commercial or counter.

            - "commercial" will return the discounted price for the commercial customer or Solutions for Small Business member.
            - "counter" will return the regular price paid by consumers.
            Defaults to "commercial" if not specified.
        expected_mailing_date
            The expected mailing date for the parcel.

            This date is used in calculations of the expected delivery date, however all rate quotes are based on the current system date.
        options
            Structure containing the list of options desired for the shipment.
        parcel_characteristics
            Details of the parcel such as weight and dimensions.
        unpackaged
            Indicates that the parcel will be unpackaged (e.g. tires)
        mailing_tube
            Indicates that the object will be shipped in a mailing tube
        oversized
            Indicates that the object has oversized dimensions. Automatically set correctly if dimensions are provided.
        services
            List of services to be used for the shipment.

        Returns
        -------
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

        >>> response = py_canada_post.rates.rating(
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
            headers=self._get_headers(),
        )

        return response

    @staticmethod
    def get_rate_by_service(
        rates: Rates,
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
        for rate in rates.rates:
            if rate.service.code == service_code:
                return rate

        return None


    @staticmethod
    def rate_to_object(response: Response):
        return RateToObject(response=response).response_to_object()

