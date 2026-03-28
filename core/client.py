from base64 import b64encode
from typing import Literal, Optional
from .services import GetRates
from requests.auth import to_native_string


class PyCanadaPost:
    def __init__(
            self,
            customer_number: int,
            api_key: str,
            environment: Literal["SANDBOX", "PRODUCTION"] = "SANDBOX",
            contract_id: Optional[int] = None,
            language: Literal["en-CA", "fr-CA"] = "en-CA"
    ) -> None:
        self.customer_number = customer_number
        self.contract_id = contract_id
        self.environment = environment
        self.language = language
        self._api_key = api_key

        self.endpoint = self._get_endpoint()
        self.headers = self._get_headers()

        self.rates = GetRates(
            headers=self.headers,
            endpoint=self.endpoint,
            customer_number=self.customer_number,
            contract_id=self.contract_id,
        )


    def _get_endpoint(self) -> str:
        endpoints = {
            "SANDBOX": "https://ct.soa-gw.canadapost.ca",
            "PRODUCTION": "https://soa-gw.canadapost.ca"
        }

        return endpoints[self.environment]

    def _get_headers(self) -> dict:
        username, password = self._api_key.split(":")

        username = username.encode("latin1")
        password = password.encode("latin1")

        return {
            "Accept-Language": self.language,
            "Authorization": "Basic " + to_native_string(b64encode(b":".join((username, password))).strip())
        }