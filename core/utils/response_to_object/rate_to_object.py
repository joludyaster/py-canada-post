from datetime import datetime
from typing import Union, Literal, Optional

from requests import Response
from ..response_to_object import ResponseToObject
from ...services.rating.types import Rate, RateAdjustment, RateOption, RateTax, RateTaxDetails, RateService, Rates

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

class GetAdjustmentsService:

    def construct_adjustments(self, price_quote: dict) -> Optional[list[RateAdjustment]]:
        adjustments = self._get_adjustments(price_quote=price_quote)
        if not adjustments:
            return None

        list_of_adjustments = []

        if isinstance(adjustments, list):
            for adjustment in adjustments:
                list_of_adjustments.append(self._construct_adjustment(adjustment=adjustment))
        else:
            list_of_adjustments.append(self._construct_adjustment(adjustment=adjustments))

        return list_of_adjustments

    @staticmethod
    def _construct_adjustment(adjustment: dict) -> RateAdjustment:
        code = adjustment[ADJUSTMENT_CODE]
        cost = float(adjustment[ADJUSTMENT_COST])
        name = adjustment[ADJUSTMENT_NAME]
        percentage_rate = float(adjustment[QUALIFIER][PERCENT])

        return RateAdjustment(
            code=code,
            cost=cost,
            name=name,
            percentage_rate=percentage_rate
        )

    @staticmethod
    def _get_adjustments(price_quote: dict) -> Optional[Union[dict, list]]:
        return price_quote.get(PRICE_DETAILS, {}).get(ADJUSTMENTS, {}).get(ADJUSTMENT, None)

class GetOptionsService:

    def construct_options(self, price_quote: dict) -> Optional[list[RateOption]]:
        options = self._get_options(price_quote=price_quote)
        if not options:
            return None

        list_of_options = []

        if isinstance(options, list):
            for option in options:
                list_of_options.append(self._construct_option(option=option))
        else:
            list_of_options.append(self._construct_option(option=options))

        return list_of_options

    @staticmethod
    def _construct_option(option: dict) -> RateOption:
        code = option[OPTION_CODE]
        name = option[OPTION_NAME]
        price = float(option[OPTION_PRICE])
        included = option[QUALIFIER][INCLUDED] == "true"

        return RateOption(
            code=code,
            name=name,
            price=price,
            included=included
        )

    @staticmethod
    def _get_options(price_quote: dict) -> Optional[Union[dict, list]]:
        return price_quote.get(PRICE_DETAILS, {}).get(OPTIONS, {}).get(OPTION, None)

class RatingService:

    def __init__(self):
        self.get_options_service = GetOptionsService()
        self.get_adjustments_service = GetAdjustmentsService()

    def construct_price_quotes(self, price_quotes: list[dict]) -> Rates:
        list_of_price_quotes = []

        for price_quote in price_quotes:
            list_of_price_quotes.append(self._construct_price_quote(price_quote=price_quote))

        return Rates(rates=list_of_price_quotes)

    def _construct_price_quote(self, price_quote: dict):
        adjustments = self.get_adjustments_service.construct_adjustments(price_quote=price_quote)
        options = self.get_options_service.construct_options(price_quote=price_quote)

        price_details = price_quote.get(PRICE_DETAILS, {})
        taxes = price_details.get(TAXES)

        gst = self._construct_tax(obj=taxes, tax_type="gst")
        hst = self._construct_tax(obj=taxes, tax_type="hst")
        pst = self._construct_tax(obj=taxes, tax_type="pst")

        service = self._construct_service(price_quote=price_quote)

        base = float(price_details.get(BASE, 0))
        due = float(price_details.get(DUE, 0))

        return Rate(
            adjustments=adjustments,
            base=base,
            due=due,
            options=options,
            taxes=RateTax(
                gst=gst,
                hst=hst,
                pst=pst
            ),
            service=service
        )

    @staticmethod
    def get_price_quotes(obj: dict) -> Union[dict, list]:
        return obj.get(PRICE_QUOTES, {}).get(PRICE_QUOTE)

    @staticmethod
    def _construct_tax(obj: dict, tax_type: Literal["gst", "hst", "pst"]) -> Optional[RateTaxDetails]:
        get_tax_type = obj.get(tax_type, {})
        if not get_tax_type:
            return None

        return RateTaxDetails(
            price=float(get_tax_type.get(TEXT, -1)),
            percentage_rate=float(get_tax_type.get(PERCENT_2, -1))
        )

    @staticmethod
    def _construct_service(price_quote: dict) -> RateService:
        service_code = price_quote[SERVICE_CODE]
        service_name = price_quote[SERVICE_NAME]

        service_standard = price_quote[SERVICE_STANDARD]
        service_am_delivery = service_standard[AM_DELIVERY] == "true"
        service_expected_delivery_date = datetime.strptime(service_standard[EXPECTED_DELIVERY_DATE], "%Y-%m-%d")
        service_expected_transit_time = int(service_standard[EXPECTED_TRANSIT_TIME])
        service_guaranteed_delivery = service_standard[GUARANTEED_DELIVERY] == "true"

        return RateService(
            code=service_code,
            name=service_name,
            am_delivery=service_am_delivery,
            expected_delivery_date=service_expected_delivery_date,
            expected_transit_time=service_expected_transit_time,
            guaranteed_delivery=service_guaranteed_delivery
        )

class RateToObject(ResponseToObject):
    def __init__(self, response: Response):
        super().__init__(response=response)
        self.rating_service = RatingService()

    def response_to_object(self):
        price_quote = self.rating_service.get_price_quotes(obj=self.parsed_response)
        if isinstance(price_quote, dict):
            return self.rating_service.construct_price_quotes(price_quotes=[price_quote])

        return self.rating_service.construct_price_quotes(price_quotes=price_quote)

