from datetime import datetime
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass(kw_only=True)
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
    option_amount: float

@dataclass(kw_only=True)
class DomesticDestination:
    postal_code: str

@dataclass(kw_only=True)
class UnitedStatesDestination:
    zip_code: str

@dataclass(kw_only=True)
class InternationalDestination:
    country_code: str
    postal_code: str

@dataclass(kw_only=True)
class Destination:
    domestic: Optional[DomesticDestination] = None
    united_states: Optional[UnitedStatesDestination] = None
    international: Optional[InternationalDestination] = None

# ===================
# PARCEL CHARACTERISTICS
# ===================
@dataclass(kw_only=True)
class Dimensions:
    length: float
    width: float
    height: float

@dataclass(kw_only=True)
class ParcelCharacteristics:
    weight: float
    dimensions: Optional[Dimensions] = None

# ===================
# RATES OBJECT
# ===================
@dataclass(kw_only=True)
class RateAdjustment:
    """
    Adjustment code

    - AUTDISC – Automation discount
    - FUELSC – Fuel surcharge
    - PROMODISC – Promotional discount (if the promo code is invalid or expired, the discount amount will show as zero under adjustment-cost)
    - PLATFMDISC – Discount for using an e-commerce platform
    - NEWREGDISC – Discount for joining the Developer Program
    - SAADJ – Service area adjustment (rate adjustment up or down for specific source and destination postal code combinations)
    """
    code: Literal[
        "AUTDISC",
        "FUELSC",
        "PROMODISC",
        "PLATFMDISC",
        "NEWREGDISC",
        "SAADJ"
    ]
    cost: float
    name: str
    percentage_rate: float

@dataclass(kw_only=True)
class RateOption:
    code: str
    name: str
    price: float
    included: bool

@dataclass(kw_only=True)
class RateTaxDetails:
    price: float
    percentage_rate: float

@dataclass(kw_only=True)
class RateTax:
    gst: RateTaxDetails
    hst: RateTaxDetails
    pst: RateTaxDetails

@dataclass(kw_only=True)
class RateService:
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
    name: str
    am_delivery: bool
    expected_delivery_date: datetime
    expected_transit_time: int
    guaranteed_delivery: bool

@dataclass(kw_only=True)
class Rate:
    adjustments: Optional[list[RateAdjustment]] = None
    base: float
    due: float
    options: Optional[list[RateOption]] = None
    taxes: Optional[RateTax] = None
    service: RateService = None

@dataclass(kw_only=True)
class Rates:
    rates: list[Rate]