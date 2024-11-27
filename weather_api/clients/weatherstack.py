import httpx

from weather_api.clients.weather import WeatherClient
from weather_api.schemas import Weather


class WeatherStackClient(WeatherClient):
    def __init__(self, url: str, api_key: str) -> None:
        self.url = url
        self.api_key = api_key

    async def get_weather_data(self, city: str) -> Weather | None:
        params = {
            "query": city,
            "access_key": self.api_key,
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
            temperature=data['current']['temperature'],
            feels_like=data['current']['feelslike'],
            pressure=data['current']['pressure'],
            humidity=data['current']['humidity'],
            wind_speed=data['current']['wind_speed']
        )
        return weather_info
