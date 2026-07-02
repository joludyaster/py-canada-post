from typing import Annotated, Literal

from cyclopts import Parameter, App

from py_canada_post.client import PyCanadaPost
from py_canada_post.services.rating.types import Service

client = PyCanadaPost.from_env()

get_service = App(
    name="get-service",
    help="Command to get details about the service based on the service code and optionally country code."
)

@get_service.command
def get_service(
    service_code: Annotated[
        Literal[
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
        ],
        Parameter(name=["service-code", "-s"], required=True)
    ],
    country_code: Annotated[
        str,
        Parameter(name=["country-code", "-c"], required=False)
    ] = None
) -> Service | None:
    """
    Function to get service based on the service code and optionally,
    country code.

    Parameters
    ----------
    service_code : Literal[
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
        Service code.
    country_code : str, optional
        Country code in a 2-letter format (e.g. JP, CA, US).

    Returns
    -------
    Service or None
        Service or None.
    """

    service = client.rating.get_service.get_service(
        service_code,
        country_code
    )

    return service
