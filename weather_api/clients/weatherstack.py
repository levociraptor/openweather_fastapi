import httpx

from weather_api.clients.weather import WeatherClient
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
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(f'Error responsse {exc.response.status_code} while requesting {exc.request.url}')
            
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
