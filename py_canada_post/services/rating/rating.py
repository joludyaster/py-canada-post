from py_canada_post.services.rating.operations.discover_services import DiscoverServices
from py_canada_post.services.rating.operations.get_rates import GetRates


class Rating:
    def __init__(self, headers: dict, endpoint: str, customer_number: int, contract_id: int = None) -> None:
        """
        Initialize class variables.

        Parameters
        ----------
        headers : dict
            Headers passed to send in a request body.
        endpoint : str
            Endpoint to send a request to.
        customer_number : int
            Customer number that was obtained from Canada Post Developer Portal.
        contract_id : int, optional
            Contract id that was obtained from Canada Post Developer Portal.
        """

        # Combine passed arguments to unpack them later.
        arguments = [self._get_headers(headers), endpoint, customer_number, contract_id]

        self.rates = GetRates(*arguments)
        self.services = DiscoverServices(*arguments)

    @staticmethod
    def _get_headers(headers: dict) -> dict:
        """
        Function to generate additional headers.

        Parameters
        ----------
        headers : dict
            Initial headers.

        Returns
        -------
        dict
            Headers.
        """

        headers = headers.copy()
        headers.update(
            {
                "Accept": "application/vnd.cpc.ship.rate-v4+xml",
                "Content-Type": "application/vnd.cpc.ship.rate-v4+xml"
            }
        )
        return headers
