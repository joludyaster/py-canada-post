from typing import Annotated
from cyclopts import Parameter, App
from py_canada_post.services.rating.types import Service
from py_canada_post.client import PyCanadaPost

client = PyCanadaPost.from_env()

discover_services = App(
    name="discover-services",
    help="Command to get available services."
)

@discover_services.command
def discover_services(
    country_code: Annotated[
        str,
        Parameter(name=["country-code", "-cc"], required=True)
    ],
    origin_postal_code: Annotated[
        str,
        Parameter(name=["origin-postal-code", "-opc"], required=False)
    ] = None,
    destination_postal_code: Annotated[
        str,
        Parameter(name=["destination-postal-code", "-dpc"], required=False)
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
        List of available services or None.
    """

    response = client.rating.services.discover_services(
        country_code,
        origin_postal_code,
        destination_postal_code
    )
    return client.rating.services.service_to_object(response)