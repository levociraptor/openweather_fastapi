import typing as t

from fastapi import Depends, Header

from weather_api.clients.openweather import OpenWeatherClient
from weather_api.clients.weatherbit import WeatherBitClient
from weather_api.clients.weatherstack import WeatherStackClient
from weather_api.config import openweather_config, weatherbit_config, weatherstack_config
from weather_api.repos.weather.database import WeatherAlchemyRepo, get_weather_alchemy_repo
from weather_api.repos.weather.database_psyco import WeatherPsycoRepo, get_weather_psyco_repo
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.services.weather import WeatherService


def get_weather_repo(
    weather_alchemy_repo: t.Annotated[WeatherAlchemyRepo, Depends(get_weather_alchemy_repo)],
    weather_psyco_repo: t.Annotated[WeatherPsycoRepo, Depends(get_weather_psyco_repo)],
    fast_sql_headers: t.Annotated[str | None, Header] = None,
) -> WeatherRepo:
    if fast_sql_headers is not None:
        return weather_psyco_repo

    return weather_alchemy_repo


def get_weather_service() -> WeatherService:
    openweather_client = OpenWeatherClient(openweather_config.url, openweather_config.api_key)
    weatherbit_client = WeatherBitClient(weatherbit_config.url, weatherbit_config.api_key)
    weatherstack_client = WeatherStackClient(weatherstack_config.url, weatherstack_config.api_key)
    weather_clients = [openweather_client, weatherbit_client, weatherstack_client]

    weather_service = WeatherService(weather_clients)
    return weather_service
