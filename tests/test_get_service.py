import pytest

class TestGetService:

    def test_get_service(self, client):
        get_service = client.rating.get_service.get_service("DOM.RP")

        assert get_service is not None

    def test_invalid_service_code(self, client):
        with pytest.raises(AttributeError):
            client.rating.get_service.get_service("G")
