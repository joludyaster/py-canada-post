from dataclasses import dataclass
from typing import Literal


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
