from datetime import datetime

from fastapi import FastAPI
import httpx

from weather_api.schemas import Weather
from weather_api.config import config
from weather_api.database import insert_weather_by_city_data, insert_weather_by_city_data_alq

app = FastAPI()


@app.get('/weather/')
def get_weather_by_city(city: str):
    params = {
        'q': city,
        'appid': config.api_key,
        'units': 'metric'
    }

    response = httpx.get(config.url, params=params)
    if response.status_code == 404:
        return {'Error': 'city not found'}

    data = response.json()

    weather = data['main']
    temperature = weather['temp']
    feels_like = weather['feels_like']
    pressure = weather['pressure']
    humidity = weather['humidity']

    wind = data['wind']
    wind_speed = wind['speed']

    weather_info = Weather(
        city=city,
        temperature=temperature,
        feels_like=feels_like,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed
    )

    insert_weather_by_city_data_alq(
        weather_info.city,
        weather_info.temperature,
        weather_info.feels_like,
        weather_info.pressure,
        weather_info.humidity,
        weather_info.wind_speed,
    )

    print(weather_info)

    return weather_info
