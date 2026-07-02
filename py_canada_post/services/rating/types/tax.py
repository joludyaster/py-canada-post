from dataclasses import dataclass


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
