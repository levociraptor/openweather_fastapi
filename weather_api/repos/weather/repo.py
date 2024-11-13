import typing as t

from weather_api.schemas import Weather


class WeatherRepo(t.Protocol):
    def insert_weather_by_city_data(
        self,
        city: str,
        temperature: float,
        feels_like: float,
        pressure: int,
        humidity: int,
        wind_speed: float,
    ) -> None:
        """Insert weather in the city."""

    def read_last_data_by_city(self, city: str) -> Weather | None:
        """Selcect weather"""
