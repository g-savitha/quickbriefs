from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class MockResponse:
    @staticmethod
    def json():
        return {}  # or whatever mocked response you want

    @staticmethod
    def raise_for_status():
        pass

    text = "Mocked text response"
    status_code = 404


def test_valid_url():
    response = client.post(
        "/scrape/", json={"url": "https://google.com"})
    assert response.status_code == 200


def test_invalid_url():
    with patch('requests.get') as mock_get:
        mock_get.return_value = MockResponse()
        response = client.post(
            "/scrape/", json={"url": "https://thisurldoesnotexist.com/"})
        assert response.status_code == 404
