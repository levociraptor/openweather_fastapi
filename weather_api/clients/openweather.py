import httpx

from weather_api.clients.weather import WeatherClient
from weather_api.config import openweather_config
from weather_api.schemas import Weather


class OpenWeatherClient(WeatherClient):
    def __init__(self, url: str, api_key: str) -> None:
        self.url = url
        self.api_key = api_key

    def get_weather_data(self, city: str) -> Weather:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }
        response = httpx.get(self.url, params=params)
        data = response.json()

        weather_info = Weather(
            city=city.lower(),
            temperature=data['main']['temp'],
            feels_like=data['main']['feels_like'],
            pressure=data['main']['pressure'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed']
        )
        return weather_info


def get_openweather_client() -> OpenWeatherClient:
    return OpenWeatherClient(openweather_config.url, openweather_config.api_key)
