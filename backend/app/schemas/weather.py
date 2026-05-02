from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    weathercode: int
    windspeed: float


class ForecastDay(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    weathercode: int


class ForecastResponse(BaseModel):
    city: str
    forecast: list[ForecastDay]
