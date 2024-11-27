from datetime import datetime, timedelta

import asyncpg
from asyncpg.connection import Connection

from weather_api.config import db_config
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather


class WeatherPsycoRepo(WeatherRepo):
    async def get_db_connection(self) -> Connection:
        return await asyncpg.connect(
            host=db_config.host,
            database='weather',
            user=db_config.username,
            password=db_config.password,
        )

    async def insert_weather_by_city_data(
            self,
            city: str,
            temperature: float,
            feels_like: float,
            pressure: float,
            humidity: int,
            wind_speed: float,
            ) -> None:

        conn = await self.get_db_connection()

        insert_query = (
            """
            INSERT INTO weather_by_city (
            city, temperature, feels_like, pressure, humidity, wind_speed, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """
        )

        await conn.execute(
            insert_query,
            city.lower(),
            temperature,
            feels_like,
            pressure,
            humidity,
            wind_speed,
            datetime.now(),
            )

        await conn.close()

    async def read_last_data_by_city(self, city: str) -> Weather | None:
        conn = await self.get_db_connection()

        select_query = """
        SELECT * FROM weather_by_city
        WHERE city = $1
        ORDER BY created_at DESC
        LIMIT 1
        """
        weather_record = await conn.fetchrow(select_query, city.lower())

        await conn.close()

        if not weather_record:
            return None

        datetime_last_request = weather_record['created_at']
        if datetime.now() - datetime_last_request < timedelta(hours=1):
            weather_info = Weather(
                city=weather_record['city'],
                temperature=weather_record['temperature'],
                feels_like=weather_record['feels_like'],
                pressure=weather_record['pressure'],
                humidity=weather_record['humidity'],
                wind_speed=weather_record['wind_speed'],
            )
            return weather_info
        return None


def get_weather_psyco_repo() -> WeatherPsycoRepo:
    return WeatherPsycoRepo()
