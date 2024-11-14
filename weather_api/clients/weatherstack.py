import httpx

from weather_api.clients.weather import WeatherClient
from weather_api.config import weather_stack_config
from weather_api.schemas import Weather


class WeatherStackClient(WeatherClient):
    def __init__(self, url: str, api_key: str) -> None:
        self.url = url
        self.api_key = api_key

    def get_weather_data(self, city: str) -> Weather:
        params = {
            "query": city,
            "access_key": self.api_key,
        }
        response = httpx.get(self.url, params=params)
        data = response.json()

        weather_info = Weather(
            city=city.lower(),
            temperature=data['current']['temperature'],
            feels_like=data['current']['feelslike'],
            pressure=data['current']['pressure'],
            humidity=data['current']['humidity'],
            wind_speed=data['current']['wind_speed']
        )
        return weather_info


def get_weatherstack_client() -> WeatherStackClient:
    return WeatherStackClient(weather_stack_config.url, weather_stack_config.api_key)
