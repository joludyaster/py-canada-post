import pytest

from py_canada_post.exceptions.exceptions import InvalidDestinationCountry, MissingOriginPostalCode


class TestServices:

    def test_services(self, client):
        services = client.rating.services.discover_services("JP")

        assert services is not None
        assert len(services) > 0

        first_service = services[0]

        assert first_service.service_code is not None
        assert first_service.service_name is not None

    def test_invalid_country_code(self, client):
        with pytest.raises(InvalidDestinationCountry) as exc_info:
            client.rating.services.discover_services("X")

        assert exc_info.value.status_code == 400

    def test_missing_origin_postal_code(self, client):
        with pytest.raises(MissingOriginPostalCode) as exc_info:
            client.rating.services.discover_services(country_code="CA", destination_postal_code="T3Z1C8")

        assert exc_info.value.status_code == 400
