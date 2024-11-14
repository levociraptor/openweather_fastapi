import typing as t

from fastapi import Depends, FastAPI

from weather_api.depends import get_weather_repo, get_weather_info
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather


app = FastAPI()


@app.get('/weather/')
def get_weather_by_city(
    city: str,
    weather_repo: t.Annotated[WeatherRepo, Depends(get_weather_repo)],

) -> Weather | dict[str, str]:

    weather_info = weather_repo.read_last_data_by_city(city.lower())

    if weather_info:
        return weather_info

    weather_info = get_weather_info(city)
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