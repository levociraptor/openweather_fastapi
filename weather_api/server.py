from fastapi import FastAPI
import httpx

from weather_api.schemas import Weather
from weather_api.config import congig

app = FastAPI()


@app.get('/weather/')
def get_weather_by_city(city: str):
    params = {
        'q': city,
        'appid': congig.api_key,
        'units': 'metric'
    }

    response = httpx.get(congig.url, params=params)
    if response.status_code == 404:
        return {'Error': 'city not found'}

    data = response.json()
    print(data)

    weather = data['main']
    temareture = weather['temp']
    feels_like = weather['feels_like']
    pressure = weather['pressure']
    humidity = weather['humidity']

    wind = data['wind']
    wind_speed = wind['speed']

    weather_info = Weather(
        city=city,
        temareture=temareture,
        feels_like=feels_like,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed
    )

    return weather_info
