from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Option:
    option_code: Literal[
        "SO",
        "COV",
        "COD",
        "PA18",
        "PA19",
        "HFP",
        "DNS",
        "LAD"
    ]
    """
    Option code.
    
    SO - Signature,
    COV - Coverage (requires qualifier),
    COD - COD (requires qualifier),
    PA18 - Proof of Age Required - 18,
    PA19 - Proof of Age Required - 19,
    HFP - Card for pickup,
    DNS - Do not safe drop,
    LAD - Leave at door - do not card.
    """
    option_amount: float
    """
    Option amount.
    
    Required for COV – the amount of insurance to be purchased.
    
    5.2 digits e.g. 99999.99.
    """


@dataclass
class DomesticDestination:
    postal_code: str
    """
    Postal code.
    
    Format ANANAN (only accepted with uppercase).
    """


@dataclass
class UnitedStatesDestination:
    zip_code: str
    """
    Zip code.
    
    Used when country code = US. Format is 5 digits or 5-4 (for extended Zip Codes).

    E.g. 12345 or 12345-6789.
    """


@dataclass
class InternationalDestination:
    country_code: str
    """
    Country code.
    
    The destination country code. 
    Standard 2-character country code (valid country code other than CA or US).
    """
    postal_code: str
    """
    Postal code.
    
    The Postal Code field can be provided if the customer would like 
    to receive a Guaranteed date for a Kahala Posts Group (KPG) country.
    """


@dataclass
class Destination:
    domestic: DomesticDestination | None = None
    """
    Domestic.
    """
    united_states: UnitedStatesDestination | None = None
    """
    United states.
    """
    international: InternationalDestination | None = None
    """
    International.
    """


@dataclass
class Dimensions:
    length: float
    """
    Length in cm.
    
    Longest dimension.

    (3.1 digits e.g. 999.9 pattern).
    """
    width: float
    """
    Width in cm.
    
    Second longest dimension.

    (3.1 digits e.g. 999.9 pattern).
    """
    height: float
    """
    Height in cm.
    
    Shortest dimension.
    
    (3.1 digits e.g. 999.9 pattern).
    """


@dataclass
class ParcelCharacteristics:
    weight: float
    """
    Weight in kg.
    	
    The weight of the parcel in kilograms.

    (99.999)
    """
    dimensions: Dimensions | None = None
    """
    Dimensions.
    """


@dataclass
class Adjustment:
    code: Literal[
        "AUTDISC",
        "FUELSC",
        "PROMODISC",
        "PLATFMDISC",
        "NEWREGDISC",
        "SAADJ"
    ]
    """
    Code.
    
    AUTDISC – Automation discount,
    FUELSC – Fuel surcharge,
    PROMODISC – Promotional discount (if the promo code is invalid or expired, the discount amount will show as zero under adjustment-cost),
    PLATFMDISC – Discount for using an e-commerce platform,
    NEWREGDISC – Discount for joining the Developer Program,
    SAADJ – Service area adjustment (rate adjustment up or down for specific source and destination postal code combinations).
    """
    cost: float
    """
    Cost. 
    	
    (9999.99 numeric).

    Amount of the adjustment in dollars and cents.
    """
    name: str
    """
    Name.
    	
    Adjustment name in preferred language.    
    """
    percentage_rate: float
    """
    Percentage rate.
    
    numeric 999.99 value 1 to 100.

    If the adjustment is based on a percentage value the percentage will be returned. E.g. fuel surcharge.
    """


@dataclass
class OptionDetails:
    code: str
    """
    Code.
    
    (10 alphanumeric).

    The unique code for the option.
    """
    name: str
    """
    Name.
    
    Option name in preferred language.
    """
    price: float
    """
    Price.
    
    (5.2 digits e.g. 99999.99 pattern).

    Cost of this option for the current parcel.
    """
    included: bool
    """
    Included.
    
    Indicates that the option is included at no charge.
    """


@dataclass
class TaxDetails:
    price: float
    """
    Price
    
    (numeric 99999.99).
    """
    percentage_rate: float
    """
    Percentage rate.
    
    numeric 999.99 value 1 to 100.

    Indicates the percentage of the tax applied to the base amount.
    """


@dataclass
class Tax:
    gst: TaxDetails | None = None
    """
    Gst.
    
    Goods and services tax.
    """
    hst: TaxDetails | None = None
    """
    Hst.
    
    Harmonized sales tax.
    """
    pst: TaxDetails | None = None
    """
    Pst.

    Provincial sales tax.
    """


@dataclass
class Service:
    code: Literal[
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
    """
    Code.
    
    DOM.RP - Regular Parcel,
    DOM.EP - Expedited Parcel,
    DOM.XP - Xpresspost,
    DOM.XP.CERT - Xpresspost Certified,
    DOM.PC - Priority,
    DOM.LIB - Library Materials,
    USA.EP - Expedited Parcel USA,
    USA.SP.AIR - Small Packet USA Air,
    USA.TP - Tracked Packet – USA,
    USA.TP.LVM - Tracked Packet – USA (LVM) (large volume mailers),
    USA.XP - Xpresspost USA,
    INT.XP - Xpresspost International,
    INT.IP.AIR - International Parcel Air,
    INT.IP.SURF - International Parcel Surface,
    INT.SP.AIR - Small Packet International Air,
    INT.SP.SURF - Small Packet International Surface,
    INT.TP - Tracked Packet – International.
    """
    name: str
    """
    Name.
    
    Service name in preferred language.
    """
    am_delivery: bool | None = None
    """
    Am delivery.
    
    Indicates whether a.m. delivery is defined as part of the service standard for this service.
    """
    expected_delivery_date: datetime | None = None
    """
    Expected delivery date.    
    
    The estimated date of delivery, starting from the expected mailing-date.
    """
    expected_transit_time: int | None = None
    """
    Expected transit time.
    
    Indicates the number of days from drop-off or pickup to 1st delivery attempt.
    """
    guaranteed_delivery: bool | None = None
    """
    Guaranteed delivery.
    
    Indicates if the delivery date is guaranteed.
    """


@dataclass
class Rate:
    base: float
    """
    Base.
    
    (numeric 99999.99).

    Base cost of the shipment before taxes.
    """
    due: float
    """
    Due.
    
    (numeric 99999.99)

    Total cost of the shipment if sent using this service including 
    the cost of selected or required options, surcharges, discounts and taxes.
    """
    adjustments: list[Adjustment] | None = None
    """
    Adjustments.
    """
    options: list[OptionDetails] | None = None
    """
    Options.
    """
    taxes: Tax | None = None
    """
    Taxes.
    """
    service: Service | None = None
    """
    Service.
    """
