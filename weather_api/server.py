import typing as t

from fastapi import Depends, FastAPI

import httpx
from httpx import HTTPStatusError, RequestError

from weather_api.config import openweather_config, weather_bit_config, weather_stack_config
from weather_api.depends import get_weather_repo
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

    weather_info = get_weather_city_from_api(city)
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


def get_weather_city_from_api(city: str) -> Weather | None:
    apis = [
        {
            "url": openweather_config.url,
            "params": {"q": city, "appid": openweather_config.api_key, "units": "metric"},
            "key_mappings": {
                "data": lambda d: d["main"],
                "temp": "temp",
                "feels_like": "feels_like",
                "pressure": "pressure",
                "humidity": "humidity",
                "wind_speed": lambda d: d["wind"]["speed"]
            }
        },
        {
            "url": weather_stack_config.url,
            "params": {"query": city, "access_key": weather_stack_config.api_key},
            "key_mappings": {
                "data": lambda d: d["current"],
                "temp": "temperature",
                "feels_like": "feelslike",
                "pressure": "pressure",
                "humidity": "humidity",
                "wind_speed": "wind_speed"
            }
        },
        {
            "url": weather_bit_config.url,
            "params": {"city": city, "key": weather_bit_config.api_key},
            "key_mappings": {
                "data": lambda d: d["data"][0],
                "temp": "temp",
                "feels_like": "app_temp",
                "pressure": "slp",
                "humidity": "rh",
                "wind_speed": "wind_spd"
            }
        }
    ]
    weathers = []
    for i in range(len(apis)):
        weathers.append(fetch_weather_data(
            apis[i]['url'],
            apis[i]['params'],
            city,
            apis[i]['key_mappings']
            ))

    weathers = [w for w in weathers if w]

    if not weathers:
        return None

    temperature = sum(weather.temperature for weather in weathers) / len(weathers)
    feels_like = sum(weather.feels_like for weather in weathers) / len(weathers)
    pressure = sum(weather.pressure for weather in weathers) // len(weathers)
    humidity = sum(weather.humidity for weather in weathers) // len(weathers)
    wind_speed = sum(weather.wind_speed for weather in weathers) / len(weathers)

    weather_info = Weather(
        city=city,
        temperature=temperature,
        feels_like=feels_like,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed,
    )

    return weather_info


def fetch_weather_data(url: str, params: dict, city: str, key_mappings: dict) -> Weather:
    try:
        response = httpx.get(url, params=params)
        data = response.json()

        weather = key_mappings['data'](data)
        weather_info = Weather(
            city=city.lower(),
            temperature=weather[key_mappings["temp"]],
            feels_like=weather[key_mappings["feels_like"]],
            pressure=weather[key_mappings["pressure"]],
            humidity=weather[key_mappings["humidity"]],
            wind_speed=key_mappings["wind_speed"](data) if callable(key_mappings["wind_speed"]) else weather[key_mappings["wind_speed"]],
        )
        return weather_info
    except (RequestError, HTTPStatusError) as e:
        print(f"Error fetching data from {url}: {e}")
        return None
