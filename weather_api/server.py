import typing as t

from fastapi import Depends, FastAPI

from weather_api.depends import get_weather_info, get_weather_repo
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather
from weather_api.services.weather import WeatherService


app = FastAPI()


@app.get('/weather/')
def get_weather_by_city(
    city: str,
    weather_repo: t.Annotated[WeatherRepo, Depends(get_weather_repo)],
    weather_getter: t.Annotated[WeatherService, Depends(get_weather_info)]
) -> Weather | dict[str, str]:

    weather_info = weather_repo.read_last_data_by_city(city)

    if weather_info:
        return weather_info

    weather_info = weather_getter.get_weather_info(city)
    if not weather_info:
        return {"Error": "City not found"}

    weather_repo.insert_weather_by_city_data(
        weather_info.city,
        weather_info.temperature,
        weather_info.feels_like,
        weather_info.pressure,
        weather_info.humidity,
        weather_info.wind_speed,
    )

    return weather_info
