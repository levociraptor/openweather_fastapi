import httpx

from weather_api.clients.weather import WeatherClient
from weather_api.schemas import Weather


class OpenWeatherClient(WeatherClient):
    def __init__(self, url: str, api_key: str) -> None:
        self.url = url
        self.api_key = api_key

    async def get_weather_data(self, city: str) -> Weather | None:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url, params=params)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                print(f'Error responsse {exc} while requesting {exc}')
                return None

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
