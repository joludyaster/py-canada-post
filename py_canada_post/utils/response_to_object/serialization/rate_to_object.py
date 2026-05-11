from requests import Response
from py_canada_post.utils.response_to_object.response_to_object import ResponseToObject
from py_canada_post.services.rating.types import Rate, RateAdjustment, RateOption, RateTax, RateTaxDetails, RateService

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
    def __init__(self, response: Response):
        super().__init__(response)

    def response_to_object(self):
        return self._construct_price_quotes(self.parsed_response)

    def _construct_price_quotes(self, obj: dict) -> list[Rate] | None:
        price_quotes = self._get_objects(obj, [PRICE_QUOTES, PRICE_QUOTE])

        if isinstance(price_quotes, list):
            return [self._construct_price_quote(price_quote) for price_quote in price_quotes]

        if isinstance(price_quotes, dict):
            return [self._construct_price_quote(price_quotes)]

        return None

    def _construct_price_quote(self, price_quote: dict):
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

    def _construct_adjustments(self, obj: dict) -> list[RateAdjustment] | None:
        return self._construct_objects(
            obj,
            [PRICE_DETAILS, ADJUSTMENTS, ADJUSTMENT],
            [ADJUSTMENT_CODE, ADJUSTMENT_COST, ADJUSTMENT_NAME, (QUALIFIER, PERCENT)],
            RateAdjustment
        )

    def _construct_options(self, obj: dict) -> list[RateOption] | None:
        return self._construct_objects(
            obj,
            [PRICE_DETAILS, OPTIONS, OPTION],
            [OPTION_CODE, OPTION_NAME, OPTION_PRICE, (QUALIFIER, INCLUDED)],
            RateOption
        )

    def _construct_service(self, obj: dict) -> RateService:
        return self._construct_object(
            obj,
            [SERVICE_CODE, SERVICE_NAME, (SERVICE_STANDARD, AM_DELIVERY), (SERVICE_STANDARD, EXPECTED_DELIVERY_DATE), (SERVICE_STANDARD, EXPECTED_TRANSIT_TIME), (SERVICE_STANDARD, GUARANTEED_DELIVERY)],
            RateService
        )

    def _construct_taxes(self, obj: dict) -> RateTax:
        taxes = []
        for tax_type in ["gst", "hst", "pst"]:
            tax = obj.get(PRICE_DETAILS, {}).get(TAXES, {}).get(tax_type)
            taxes.append(self._construct_object(tax, [TEXT, PERCENT_2], RateTaxDetails))

        return RateTax(
            gst=taxes[0],
            hst=taxes[1],
            pst=taxes[2]
        )