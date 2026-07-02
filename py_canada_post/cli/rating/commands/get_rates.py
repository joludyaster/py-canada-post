import dataclasses
import typing
from datetime import datetime
from typing import Annotated, Literal

from cyclopts import Parameter, App

from py_canada_post.client import PyCanadaPost
from py_canada_post.services.rating.types import Destination, Option, ParcelCharacteristics, Rate

client = PyCanadaPost.from_env()

get_rates = App(
    name="get-rates",
    help="Command to get rates."
)


def options_converter(type_, tokens):
    inner_type = typing.get_args(type_)[0]
    results = []
    current = {}
    fields = dataclasses.fields(inner_type)

    for token in tokens:
        if token.index == 0 and current:
            results.append(inner_type(**current))
            current = {}

        field = fields[token.index]
        # Unwrap Optional[X] -> X
        field_type = typing.get_args(field.type)[0] if typing.get_args(field.type) else field.type

        # Cast to the field's type
        if field_type is float:
            current[field.name] = float(token.value)
        elif field_type is int:
            current[field.name] = int(token.value)
        elif field_type is bool:
            current[field.name] = token.value.lower() in ("true", "1", "yes")
        else:
            current[field.name] = token.value

    if current:
        results.append(inner_type(**current))

    return results


@get_rates.command
def get_rates(
    origin_postal_code: Annotated[
        str,
        Parameter(name=["origin-postal-code", "-o"], required=True)
    ],
    destination: Annotated[
        Destination,
        Parameter(name=["destination", "-d"], required=True)
    ],
    promo_code: Annotated[
        str,
        Parameter(name=["promo-code", "-p"], required=False)
    ] = None,
    quote_type: Annotated[
        Literal["commercial", "counter"],
        Parameter(name=["quote-type", "-q"], required=False)
    ] = "commercial",
    expected_mailing_date: Annotated[
        datetime,
        Parameter(name=["expected-mailing-date", "-m"], required=False)
    ] = None,
    options: Annotated[
        list[Option],
        Parameter(name=["options", "-O"], required=False, converter=options_converter, consume_multiple=True)
    ] = None,
    parcel_characteristics: Annotated[
        ParcelCharacteristics,
        Parameter(name=["parcel-characteristics", "-c"], required=False)
    ] = None,
    unpackaged: Annotated[
        bool,
        Parameter(name=["unpackaged", "-u"], required=False)
    ] = False,
    mailing_tube: Annotated[
        bool,
        Parameter(name=["mailing-tube", "-t"], required=False)
    ] = False,
    oversized: Annotated[
        bool,
        Parameter(name=["oversized", "-z"], required=False)
    ] = False,
    services: Annotated[
        list[Literal[
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
        ]],
        Parameter(name=["services", "-s"], required=False, consume_multiple=True)
    ] = None
) -> list[Rate] | None:
    """
    Command to get rates.

    Parameters
    ----------
    origin_postal_code : str
        Postal Code from which the parcel will be sent.
        Format ANANAN (only accepted with uppercase)
    destination : Destination
        Defines the destination of the parcel.
    promo_code : str, optional
        If you have a promotional discount code, enter it here. The discount amount will be returned in the response under the adjustment structure.
    quote_type : Literal["commercial", "counter"], default "commercial"
        Either commercial or counter.

        - "commercial" will return the discounted price for the commercial customer or Solutions for Small Business member.
        - "counter" will return the regular price paid by consumers.
        Defaults to "commercial" if not specified.
    expected_mailing_date : datetime, optional
        The expected mailing date for the parcel.

        This date is used in calculations of the expected delivery date, however all rate quotes are based on the current system date.
    options : list[Option], optional
        Structure containing the list of options desired for the shipment.
    parcel_characteristics : ParcelCharacteristics, optional
        Details of the parcel such as weight and dimensions.
    unpackaged : bool, default False
        Indicates that the parcel will be unpackaged (e.g. tires)
    mailing_tube : bool, default False
        Indicates that the object will be shipped in a mailing tube
    oversized : bool, default False
        Indicates that the object has oversized dimensions. Automatically set correctly if dimensions are provided.
    services : list[Literal[
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
    ]], optional
        List of services to be used for the shipment.

    Returns
    -------
    list[Rate] or None
        List of rates or None.
    """

    rates = client.rating.rates.get_rates(
        origin_postal_code,
        destination,
        promo_code,
        quote_type,
        expected_mailing_date,
        options,
        parcel_characteristics,
        unpackaged,
        mailing_tube,
        oversized,
        services
    )
    return rates
