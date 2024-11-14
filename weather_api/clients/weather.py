import typing as t

from weather_api.schemas import Weather


class WeatherClient(t.Protocol):
    def get_weather_data(self, city: str) -> Weather:
        """Return Weather pydantic model"""
