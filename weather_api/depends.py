import typing as t

from fastapi import Depends, Header

from weather_api.repos.weather.database import WeatherAlchemyRepo, get_weather_alchemy_repo
from weather_api.repos.weather.database_psyco import WeatherPsycoRepo, get_weather_psyco_repo
from weather_api.repos.weather.repo import WeatherRepo


def get_weather_repo(
    weather_alchemy_repo: t.Annotated[WeatherAlchemyRepo, Depends(get_weather_alchemy_repo)],
    weather_psyco_repo: t.Annotated[WeatherPsycoRepo, Depends(get_weather_psyco_repo)],
    fast_sql_headers: t.Annotated[str | None, Header] = None,
) -> WeatherRepo:
    if fast_sql_headers is not None:
        return weather_psyco_repo

    return weather_alchemy_repo
