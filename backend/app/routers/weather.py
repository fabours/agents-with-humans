import httpx
from fastapi import APIRouter, HTTPException, Query

from app.schemas.weather import WeatherResponse

router = APIRouter()

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@router.get("/weather/current", response_model=WeatherResponse)
async def get_current_weather(city: str = Query(..., min_length=1)):
    async with httpx.AsyncClient() as client:
        # Step 1: Geocode city name to lat/lon
        try:
            geo_response = await client.get(
                GEOCODING_URL,
                params={"name": city, "count": 1, "language": "en", "format": "json"},
            )
            geo_response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Upstream geocoding API unavailable")

        results = geo_response.json().get("results", [])
        if not results:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")

        latitude = results[0]["latitude"]
        longitude = results[0]["longitude"]

        # Step 2: Fetch current weather
        try:
            forecast_response = await client.get(
                FORECAST_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,weathercode,windspeed_10m",
                    "timezone": "auto",
                },
            )
            forecast_response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Upstream forecast API unavailable")

        current = forecast_response.json().get("current", {})

    return WeatherResponse(
        city=city,
        temperature=current["temperature_2m"],
        weathercode=current["weathercode"],
        windspeed=current["windspeed_10m"],
    )
