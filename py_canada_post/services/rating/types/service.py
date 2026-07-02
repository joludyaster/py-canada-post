from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .option import Option


@dataclass
class AttributeRestriction:
    min_value: float
    """
    Min value.
    """
    max_value: float
    """
    Max value.
    """


@dataclass
class DimensionalRestrictions:
    length: AttributeRestriction | None = None
    """
    Length.

    Specifies the dimension range of the longest dimension of an item in cm.
    """
    width: AttributeRestriction | None = None
    """
    Width.

    Specifies the dimension range of the second longest dimension of an item in cm.
    """
    height: AttributeRestriction | None = None
    """
    Height.

    Specifies the dimension range of the shortest dimension of an item in cm.
    """
    length_plus_girth_max: float | None = None
    """
    Length plus girth max.

    Maximum calculated value of length + 2*width + 2*height in cm.
    """
    length_height_width_sum_max: float | None = None
    """
    Length height width sum max.

    Maximum value of length + width + height in cm.
    """
    oversize_limit: float | None = None
    """
    Oversize limit.

    If any dimension exceeds this limit an oversize fee will apply to the shipment (cm).
    """


@dataclass
class Restrictions:
    weight_restriction: AttributeRestriction | None = None
    """
    Weight restriction.

    Details the weight restrictions of items shipped via this service.
    """
    dimensional_restrictions: DimensionalRestrictions | None = None
    """
    Dimensional restrictions.

    Details the dimension restrictions of items shipped via this service.
    """
    density_factor: float | None = None
    """
    Density factor.

    Standard density factor used to calculate volumetric equivalent of actual weight (VE).
    Note: Canada Post can use another factor to calculate the volumetric equivalent, depending on your parcels agreement.
    """
    can_ship_in_mailing_tube: bool | None = None
    """
    Can ship in mailing tube.

    True indicates that parcels shipped with this service can be shipped in a mailing tube (option CYL can be used).
    """
    can_ship_unpackaged: bool | None = None
    """
    Can ship unpackaged.

    True indicates that parcels shipped with this service can be shipped unpackaged (option UP can be used).
    """
    allowed_as_return_service: bool | None = None
    """
    Allowed as return service.

    True indicates that this service can be used in the return-spec of a Create Shipment request.
    """


@dataclass
class Service:
    service_code: Literal[
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
    Service code.

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
    service_name: str | None = None
    """
    Service name.

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
    comment: str | None = None
    """
    Comment.

    Coverage message stating the maximum amount of coverage included with 
    this service (which can be none); only returned on a few U.S. and international services 
    where additional coverage cannot be purchased.

    Only applicable to schema version 2 and higher.
    """
    options: list[Option] | None = None
    """
    Options.

    List of options available/applicable to this service.
    """
    restrictions: Restrictions | None = None
    """
    Restrictions.

    Details the weight and size restrictions of parcels shipped via this service.
    """
