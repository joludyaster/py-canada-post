from requests import Response

from py_canada_post.services.rating.types import Rate, Adjustment, Option, Tax, TaxDetails, Service
from py_canada_post.utils.response_to_object.response_to_object import ResponseToObject

ADJUSTMENTS = "adjustments"
ADJUSTMENT = "adjustment"
ADJUSTMENT_CODE = "adjustment-code"
ADJUSTMENT_COST = "adjustment-cost"
ADJUSTMENT_NAME = "adjustment-name"
QUALIFIER = "qualifier"
PERCENT = "percent"

PRICE_DETAILS = "price-details"

OPTIONS = "options"
OPTION = "option"
OPTION_CODE = "option-code"
OPTION_NAME = "option-name"
OPTION_PRICE = "option-price"
INCLUDED = "included"

TAXES = "taxes"
BASE = "base"
DUE = "due"

PRICE_QUOTES = "price-quotes"
PRICE_QUOTE = "price-quote"

TEXT = "#text"
PERCENT_2 = "@percent"

SERVICE_CODE = "service-code"
SERVICE_NAME = "service-name"
SERVICE_STANDARD = "service-standard"
AM_DELIVERY = "am-delivery"
EXPECTED_DELIVERY_DATE = "expected-delivery-date"
EXPECTED_TRANSIT_TIME = "expected-transit-time"
GUARANTEED_DELIVERY = "guaranteed-delivery"


class RateToObject(ResponseToObject):
    def __init__(self, response: Response) -> None:
        """
        Initialize class variables.

        Parameters
        ----------
        response : Response
            Response object.
        """

        super().__init__(response)

    def response_to_object(self) -> list[Rate] | None:
        """
        Main function to deserialize xml response object.

        Returns
        -------
        list[Rate] or None
            List of rates or None.
        """

        return self._construct_price_quotes(self.parsed_response)

    def _construct_price_quotes(self, obj: dict) -> list[Rate] | None:
        """
        Function to generate price quotes based on the object provided.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        list[Rate] or None
            List of rates of None.
        """

        price_quotes = self._get_objects(obj, [PRICE_QUOTES, PRICE_QUOTE])

        if isinstance(price_quotes, list):
            return [self._construct_price_quote(price_quote) for price_quote in price_quotes]

        if isinstance(price_quotes, dict):
            return [self._construct_price_quote(price_quotes)]

        return None

    def _construct_price_quote(self, price_quote: dict) -> Rate:
        """
        Function that gathers all other properties of the Rate and combines them all together.

        Parameters
        ----------
        price_quote : dict
            Price quote object.

        Returns
        -------
        Rate
            Rate with all the properties combined.
        """

        adjustments = self._construct_adjustments(price_quote)
        options = self._construct_options(price_quote)
        taxes = self._construct_taxes(price_quote)
        service = self._construct_service(price_quote)

        base = float(price_quote.get(PRICE_DETAILS, {}).get(BASE, 0))
        due = float(price_quote.get(PRICE_DETAILS, {}).get(DUE, 0))

        return Rate(
            adjustments=adjustments,
            base=base,
            due=due,
            options=options,
            taxes=taxes,
            service=service
        )

    def _construct_adjustments(self, obj: dict) -> list[Adjustment] | None:
        """
        Function to construct adjustments.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        list[Adjustment] or None
            List of adjustments or None.
        """

        return self._construct_objects(
            obj,
            [PRICE_DETAILS, ADJUSTMENTS, ADJUSTMENT],
            [ADJUSTMENT_CODE, ADJUSTMENT_COST, ADJUSTMENT_NAME, (QUALIFIER, PERCENT)],
            Adjustment
        )

    def _construct_options(self, obj: dict) -> list[Option] | None:
        """
        Function to construct options.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        list[OptionDetails] or None
            List of options or None.
        """

        return self._construct_objects(
            obj,
            [PRICE_DETAILS, OPTIONS, OPTION],
            [OPTION_CODE, None, OPTION_PRICE, (QUALIFIER, INCLUDED), OPTION_NAME],
            Option
        )

    def _construct_service(self, obj: dict) -> Service:
        """
        Function to construct service.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        Service
        """

        return self._construct_object(
            obj,
            [SERVICE_CODE, SERVICE_NAME, (SERVICE_STANDARD, AM_DELIVERY), (SERVICE_STANDARD, EXPECTED_DELIVERY_DATE),
             (SERVICE_STANDARD, EXPECTED_TRANSIT_TIME), (SERVICE_STANDARD, GUARANTEED_DELIVERY)],
            Service
        )

    def _construct_taxes(self, obj: dict) -> Tax:
        """
        Function to construct taxes.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        Tax
        """

        taxes = {}
        for tax_type in ["gst", "hst", "pst"]:
            tax = obj.get(PRICE_DETAILS, {}).get(TAXES, {}).get(tax_type)
            taxes[tax_type] = self._construct_object(tax, [TEXT, PERCENT_2], TaxDetails)

        return Tax(
            gst=taxes["gst"],
            hst=taxes["hst"],
            pst=taxes["pst"]
        )
