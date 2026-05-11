import os

from base64 import b64encode
from typing import Literal
from py_canada_post.services.rating.rating import Rating
from requests.auth import to_native_string
from dotenv import load_dotenv

load_dotenv()

class PyCanadaPost:
    def __init__(
        self,
        customer_number: int,
        api_key: str,
        environment: Literal["SANDBOX", "PRODUCTION"] = "SANDBOX",
        contract_id: int = None,
        language: Literal["en-CA", "fr-CA"] = "en-CA"
    ) -> None:
        self.customer_number = customer_number
        self.contract_id = contract_id
        self.environment = environment
        self.language = language
        self._api_key = api_key

        self.endpoint = self._get_endpoint()
        self.headers = self._get_headers()

        self.rating = Rating(self.headers, self.endpoint, self.customer_number, self.contract_id)


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

    @classmethod
    def from_env(cls):
        customer_number = os.getenv("CUSTOMER_NUMBER", None)
        api_key = os.getenv("API_KEY", None)
        contract_id = os.getenv("CONTRACT_ID", None)

        if not customer_number or not api_key or not contract_id:
            raise AssertionError(
                "Missing .env variables. "
                "Please make sure you have CUSTOMER_NUMBER, API_KEY and CONTRACT_ID set up in your .env"
            )

        return cls(
            customer_number=int(customer_number),
            api_key=api_key,
            contract_id=int(contract_id),
        )