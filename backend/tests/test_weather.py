from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_mock_response(json_data: dict, status_code: int = 200):
    mock = MagicMock()
    mock.json.return_value = json_data
    mock.status_code = status_code
    mock.raise_for_status = MagicMock()
    return mock


GEO_SUCCESS = {"results": [{"latitude": 45.5, "longitude": -73.5}]}
GEO_NOT_FOUND = {"results": []}
FORECAST_SUCCESS = {
    "current": {
        "temperature_2m": 18.5,
        "weathercode": 3,
        "windspeed_10m": 12.0,
    }
}


@patch("app.routers.weather.httpx.AsyncClient")
def test_get_weather_success(mock_client_class):
    mock_get = AsyncMock(
        side_effect=[
            make_mock_response(GEO_SUCCESS),
            make_mock_response(FORECAST_SUCCESS),
        ]
    )
    mock_instance = MagicMock()
    mock_instance.get = mock_get
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=False)
    mock_client_class.return_value = mock_instance

    response = client.get("/api/weather/current?city=Montreal")

    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Montreal"
    assert data["temperature"] == 18.5
    assert data["weathercode"] == 3
    assert data["windspeed"] == 12.0


@patch("app.routers.weather.httpx.AsyncClient")
def test_get_weather_city_not_found(mock_client_class):
    mock_get = AsyncMock(return_value=make_mock_response(GEO_NOT_FOUND))
    mock_instance = MagicMock()
    mock_instance.get = mock_get
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=False)
    mock_client_class.return_value = mock_instance

    response = client.get("/api/weather/current?city=Fakecityxyz")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_weather_missing_city_param():
    response = client.get("/api/weather/current")
    assert response.status_code == 422
