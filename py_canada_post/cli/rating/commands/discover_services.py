from typing import Annotated

from cyclopts import Parameter, App

from py_canada_post.client import PyCanadaPost
from py_canada_post.services.rating.types import Service

client = PyCanadaPost.from_env()

discover_services = App(
    name="discover-services",
    help="Command to get available services."
)


@discover_services.command
def discover_services(
    country_code: Annotated[
        str,
        Parameter(name=["country-code", "-c"], required=True)
    ],
    origin_postal_code: Annotated[
        str,
        Parameter(name=["origin-postal-code", "-o"], required=False)
    ] = None,
    destination_postal_code: Annotated[
        str,
        Parameter(name=["destination-postal-code", "-d"], required=False)
    ] = None
) -> list[Service] | None:
    """
    Command to get available services.

    Parameters
    ----------
    country_code : str
        Country code in a 2-letter format (e.g. JP, CA, US).
    origin_postal_code : str, optional
        Origin postal code where the package will be sent from.
    destination_postal_code : str, optional
        Destination postal code where the package will be delivered to.

    Returns
    -------
    list[Service] | None
        List of services or None.
    """

    services = client.rating.services.discover_services(
        country_code,
        origin_postal_code,
        destination_postal_code
    )
    return services
