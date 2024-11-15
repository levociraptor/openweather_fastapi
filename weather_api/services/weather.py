from weather_api.clients.weather import WeatherClient
from weather_api.schemas import Weather


class WeatherService():
    def __init__(self, clients: list[WeatherClient]) -> None:
        self.clients = clients

    async def get_weather_info(self, city: str) -> Weather:
        weathers = []
        for client in self.clients:
            if client is not None:
                weather = await client.get_weather_data(city)
                weathers.append(weather)

        weather_info = Weather(
            city=city,
            temperature=sum([weather.temperature for weather in weathers]) / 3,
            feels_like=sum([weather.feels_like for weather in weathers]) / 3,
            pressure=sum([weather.pressure for weather in weathers]) // 3,
            humidity=sum([weather.humidity for weather in weathers]) // 3,
            wind_speed=sum([weather.wind_speed for weather in weathers]) / 3,
        )

        return weather_info
