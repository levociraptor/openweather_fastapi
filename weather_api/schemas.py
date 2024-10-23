from pydantic import BaseModel


class Weather(BaseModel):
    city: str
    temareture: float
    feels_like: float
    pressure: int
    humidity: int
    wind_speed: float
