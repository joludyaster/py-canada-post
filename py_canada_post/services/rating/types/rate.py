from dataclasses import dataclass

from .adjustment import Adjustment
from .option import Option
from .tax import Tax
from .service import Service


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
    options: list[Option] | None = None
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
