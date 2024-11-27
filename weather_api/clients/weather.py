import typing as t

from weather_api.schemas import Weather


class WeatherClient(t.Protocol):
    async def get_weather_data(self, city: str) -> Weather | None:
        """Return Weather pydantic model"""
