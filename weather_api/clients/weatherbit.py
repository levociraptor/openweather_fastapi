import httpx

from weather_api.clients.weather import WeatherClient
from weather_api.schemas import Weather


class WeatherBitClient(WeatherClient):
    def __init__(self, url: str, api_key: str) -> None:
        self.url = url
        self.api_key = api_key

    async def get_weather_data(self, city: str) -> Weather:
        params = {
            "city": city,
            "key": self.api_key,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(f'Error responsse {exc.response.status_code} while requesting {exc.request.url}')

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
