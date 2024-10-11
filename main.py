from fastapi import FastAPI
import requests
from dotenv import load_dotenv

import os

from models import WeatherResponse

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = FastAPI()


@app.get('/weather/')
def get_weather_by_city(city: str):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric' 
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 404:
        return {'Error': 'city not found'}

    data = response.json()

    weather = data['main']
    temareture = weather['temp']
    feels_like = weather['feels_like']
    pressure = weather['pressure']
    humidity = weather['humidity']

    wind = data['wind']
    wind_speed = wind['speed']

    weather_info = WeatherResponse(
        city=city,
        temareture=temareture,
        feels_like=feels_like,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed
    )

    return weather_info
