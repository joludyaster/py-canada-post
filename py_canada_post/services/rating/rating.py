from py_canada_post.services.rating.operations.discover_services import DiscoverServices
from py_canada_post.services.rating.operations.get_rates import GetRates


class Rating:
    def __init__(self, headers: dict, endpoint: str, customer_number: int, contract_id: int = None):
        arguments = [self._get_headers(headers), endpoint, customer_number, contract_id]

        self.rates = GetRates(*arguments)
        self.services = DiscoverServices(*arguments)

    @staticmethod
    def _get_headers(headers: dict) -> dict:
        headers = headers.copy()
        headers.update(
            {
                "Accept": "application/vnd.cpc.ship.rate-v4+xml",
                "Content-Type": "application/vnd.cpc.ship.rate-v4+xml"
            }
        )
        return headers