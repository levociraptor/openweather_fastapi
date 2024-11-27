import typing as t

from weather_api.schemas import Weather


class WeatherRepo(t.Protocol):
    async def insert_weather_by_city_data(
        self,
        city: str,
        temperature: float,
        feels_like: float,
        pressure: float,
        humidity: int,
        wind_speed: float,
    ) -> None:
        """Insert weather in the city."""

    async def read_last_data_by_city(self, city: str) -> Weather | None:
        """Selcect weather"""
