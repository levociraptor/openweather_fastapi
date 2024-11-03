from pydantic import BaseModel


class Weather(BaseModel):
    city: str
    temperature: float
    feels_like: float
    pressure: int
    humidity: int
    wind_speed: float
