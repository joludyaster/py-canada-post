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
    option_amount: float | None = None
    """
    Option amount.

    Required for COV – the amount of insurance to be purchased.

    5.2 digits e.g. 99999.99.
    """
    price: float | None = None
    """
    Price.

    (5.2 digits e.g. 99999.99 pattern).

    Cost of this option for the current parcel.
    """
    included: bool | None = None
    """
    Included.

    Indicates that the option is included at no charge.
    """
    option_name: str | None = None
    """
    Name.
    
    Option name in language of choice.
    """
    mandatory: bool | None = None
    """
    Mandatory
    
    Indicates whether this option is mandatory for the service.
    """
    qualifier_required: bool | None = None
    """
    Qualifier required.
    
    True indicates that this option if selected must include a qualifier on the option. 
    This is true for insurance (COV) and collect on delivery (COD) options.
    """
    qualifier_max: int | None = None
    """
    Qualifier max.
    
    Numeric – indicates the maximum value of the qualifier for this service. 
    The maximum value of a qualifier may differ between services. 
    This is specific to the insurance (COV) option.
    """
