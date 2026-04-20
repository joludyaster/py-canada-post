from typing import Optional

from .discover_services import DiscoverServices
from .get_rates import GetRates


class Rating:
    def __init__(self, headers: dict, endpoint: str, customer_number: int, contract_id: Optional[int] = None):
        self.rates = GetRates(
            headers=self._get_headers(headers=headers),
            endpoint=endpoint,
            customer_number=customer_number,
            contract_id=contract_id,
        )
        self.services = DiscoverServices(
            headers=self._get_headers(headers=headers),
            endpoint=endpoint,
            customer_number=customer_number,
            contract_id=contract_id,
        )

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