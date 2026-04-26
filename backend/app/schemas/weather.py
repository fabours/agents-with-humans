from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    weathercode: int
    windspeed: float
