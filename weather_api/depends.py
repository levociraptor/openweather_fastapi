import typing as t

from fastapi import Depends, Header

from weather_api.clients.openweather import get_openweather_client
from weather_api.clients.weatherbit import get_weatherbit_client
from weather_api.clients.weatherstack import get_weatherstack_client
from weather_api.repos.weather.database import WeatherAlchemyRepo, get_weather_alchemy_repo
from weather_api.repos.weather.database_psyco import WeatherPsycoRepo, get_weather_psyco_repo
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather


def get_weather_repo(
    weather_alchemy_repo: t.Annotated[WeatherAlchemyRepo, Depends(get_weather_alchemy_repo)],
    weather_psyco_repo: t.Annotated[WeatherPsycoRepo, Depends(get_weather_psyco_repo)],
    fast_sql_headers: t.Annotated[str | None, Header] = None,
) -> WeatherRepo:
    if fast_sql_headers is not None:
        return weather_psyco_repo

    return weather_alchemy_repo


def get_weather_info(city: str) -> Weather:
    openweather = get_openweather_client()
    openweather_weather_info = openweather.get_weather_data(city)

    weatherstack = get_weatherstack_client()
    weatherstack_weather_info = weatherstack.get_weather_data(city)

    weatherbit = get_weatherbit_client()
    weatherbit_weather_info = weatherbit.get_weather_data(city)

    weathers_info = [openweather_weather_info, weatherstack_weather_info, weatherbit_weather_info]

    weather_info = Weather(
        city=city,
        temperature=sum([weather.temperature for weather in weathers_info]) / 3,
        feels_like=sum([weather.feels_like for weather in weathers_info]) / 3,
        pressure=sum([weather.pressure for weather in weathers_info]) // 3,
        humidity=sum([weather.humidity for weather in weathers_info]) // 3,
        wind_speed=sum([weather.wind_speed for weather in weathers_info]) / 3,
    )

    return weather_info
