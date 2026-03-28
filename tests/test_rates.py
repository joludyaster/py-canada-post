import os
from dotenv import load_dotenv

from core.client import PyCanadaPost
from core.services.rating.types import (
    Destination,
    DomesticDestination,
    ParcelCharacteristics,
)

load_dotenv()


def test_get_rates():
    environment = "SANDBOX"

    client = PyCanadaPost(
        customer_number=int(os.getenv("CUSTOMER_NUMBER")),
        api_key=os.getenv(f"API_KEY_{environment}"),
        contract_id=int(os.getenv("CONTRACT_ID")),
    )

    response = client.rates.get_rates(
        origin_postal_code="E4M8S3",
        destination=Destination(
            domestic=DomesticDestination(
                postal_code="T3Z1C8"
            )
        ),
        parcel_characteristics=ParcelCharacteristics(
            weight=23.5
        ),
    )

    assert response.status_code == 200

    rates = client.rates.rate_to_object(response)

    assert rates is not None
    assert len(rates.rates) > 0

    first_quote = rates.rates[0]

    assert first_quote.service.code is not None
    assert first_quote.service.name is not None