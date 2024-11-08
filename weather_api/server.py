from datetime import datetime, timedelta

from fastapi import FastAPI, Depends
import httpx

from weather_api.schemas import Weather
from weather_api.config import config
from weather_api.database import insert_weather_by_city_data_alq, read_last_data_by_city_alq
from weather_api.database_psyco import read_last_data_by_city, insert_weather_by_city_data
from weather_api.depends import check_fast_sql_headers

app = FastAPI()


@app.get('/weather/')
def get_weather_by_city(city: str, has_fast_sql_headers: bool = Depends(check_fast_sql_headers)):
    if has_fast_sql_headers:
        last_data = read_last_data_by_city(city.lower())
        print(last_data)
        if last_data:
            datetime_last_request = last_data['created_at']
            if datetime.now() - datetime_last_request < timedelta(hours=1):
                weather_info = Weather(
                    city=last_data['city'],
                    temperature=last_data['temperature'],
                    feels_like=last_data['feels_like'],
                    pressure=last_data['pressure'],
                    humidity=last_data['humidity'],
                    wind_speed=last_data['wind_speed']
                )
                return weather_info

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
            city=city.lower(),
            temperature=temperature,
            feels_like=feels_like,
            pressure=pressure,
            humidity=humidity,
            wind_speed=wind_speed
        )

        insert_weather_by_city_data(
            weather_info.city,
            weather_info.temperature,
            weather_info.feels_like,
            weather_info.pressure,
            weather_info.humidity,
            weather_info.wind_speed,
        )

        return weather_info

    last_data = read_last_data_by_city_alq(city.lower())
    if last_data:
        datetime_last_request = last_data[-1]
        if datetime.now() - datetime_last_request < timedelta(hours=1):
            weather_info = Weather(
                city=last_data[1],
                temperature=last_data[2],
                feels_like=last_data[3],
                pressure=last_data[4],
                humidity=last_data[5],
                wind_speed=last_data[6]
            )
            return weather_info

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
        city=city.lower(),
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

    return weather_info
