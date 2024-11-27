import typing as t

from fastapi import Depends, FastAPI

from weather_api.depends import get_weather_repo, get_weather_service
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather
from weather_api.services.weather import WeatherService


app = FastAPI()


@app.get('/weather/')
async def get_weather_by_city(
    city: str,
    weather_repo: t.Annotated[WeatherRepo, Depends(get_weather_repo)],
    weather_getter: t.Annotated[WeatherService, Depends(get_weather_service)]
) -> Weather | dict[str, str]:

    weather_info = await weather_repo.read_last_data_by_city(city)

    if weather_info:
        return weather_info

    weather_service = await weather_getter.get_weather_info(city)
    if not weather_service:
        return {"Error": "City not found"}

    await weather_repo.insert_weather_by_city_data(
        weather_service.city,
        weather_service.temperature,
        weather_service.feels_like,
        weather_service.pressure,
        weather_service.humidity,
        weather_service.wind_speed,
    )

    return weather_service
