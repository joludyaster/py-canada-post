import pytest

from py_canada_post.exceptions.exceptions import ServerError
from py_canada_post.services.rating.types import (
    Destination,
    DomesticDestination,
    ParcelCharacteristics, Dimensions,
)

class TestRates:

    def test_get_rates(self, client):

        response = client.rating.rates.get_rates(
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

        rates = client.rating.rates.rate_to_object(response)

        assert rates is not None
        assert len(rates) > 0

        first_quote = rates[0]

        assert first_quote.service.code is not None
        assert first_quote.service.name is not None

    def test_invalid_postal_code(self, client):
        with pytest.raises(ServerError) as exc_info:
            client.rating.rates.get_rates(
                origin_postal_code="E4M8S",  # invalid
                destination=Destination(
                    domestic=DomesticDestination(
                        postal_code="T3Z1C8"
                    )
                ),
                parcel_characteristics=ParcelCharacteristics(
                    weight=23.5
                ),
            )

        assert exc_info.value.status_code == 400
        assert "PostalCodeType" in exc_info.value.mitigation


    def test_invalid_parcel_characteristics(self, client):
        with pytest.raises(ServerError) as exc_info:
            client.rating.rates.get_rates(
                origin_postal_code="E4M8S3",  # invalid
                destination=Destination(
                    domestic=DomesticDestination(
                        postal_code="T3Z1C8"
                    )
                ),
                parcel_characteristics=ParcelCharacteristics(
                    weight=500,
                    dimensions=Dimensions(
                        length=500,
                        height=500,
                        width=500
                    )
                ),
            )

        assert exc_info.value.status_code == 400

        for char in ["weight", "length", "height", "width"]:
            check_message = f"{char} is not a valid"
            if check_message in exc_info.value.mitigation:
                assert f"{char} is not a valid" in exc_info.value.mitigation
