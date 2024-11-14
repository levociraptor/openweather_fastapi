import httpx

from weather_api.clients.weather import WeatherClient
from weather_api.config import weather_bit_config
from weather_api.schemas import Weather


class WeatherBitClient(WeatherClient):
    def __init__(self, url: str, api_key: str) -> None:
        self.url = url
        self.api_key = api_key

    def get_weather_data(self, city: str) -> Weather:
        params = {
            "city": city,
            "key": self.api_key,
        }
        response = httpx.get(self.url, params=params)
        data = response.json()

        weather_info = Weather(
            city=city.lower(),
            temperature=data['data'][0]['temp'],
            feels_like=data['data'][0]['app_temp'],
            pressure=data['data'][0]['slp'],
            humidity=data['data'][0]['rh'],
            wind_speed=data['data'][0]['wind_spd']
        )
        return weather_info


def get_weatherbit_client() -> WeatherBitClient:
    return WeatherBitClient(weather_bit_config.url, weather_bit_config.api_key)
