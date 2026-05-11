from datetime import datetime
from dataclasses import dataclass
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
    option_amount: float

@dataclass
class DomesticDestination:
    postal_code: str

@dataclass
class UnitedStatesDestination:
    zip_code: str

@dataclass
class InternationalDestination:
    country_code: str
    postal_code: str

@dataclass
class Destination:
    domestic: DomesticDestination | None = None
    united_states: UnitedStatesDestination | None = None
    international: InternationalDestination | None = None

# ===================
# PARCEL CHARACTERISTICS
# ===================
@dataclass
class Dimensions:
    length: float
    width: float
    height: float

@dataclass
class ParcelCharacteristics:
    weight: float
    dimensions: Dimensions | None = None

# ===================
# RATES OBJECT
# ===================
@dataclass
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

@dataclass
class RateOption:
    code: str
    name: str
    price: float
    included: bool

@dataclass
class RateTaxDetails:
    price: float
    percentage_rate: float

@dataclass
class RateTax:
    gst: RateTaxDetails | None = None
    hst: RateTaxDetails | None = None
    pst: RateTaxDetails | None = None

@dataclass
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

@dataclass
class Rate:
    base: float
    due: float
    adjustments: list[RateAdjustment] | None = None
    options: list[RateOption] | None = None
    taxes: RateTax | None = None
    service: RateService | None = None

# ==========================
# SERVICES
# ==========================
@dataclass
class Service:
    code: str
    name: str
    link: str
