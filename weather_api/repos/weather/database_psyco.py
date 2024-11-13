from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import RealDictCursor

from weather_api.config import db_config
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather


# TODO need refactor
class WeatherPsycoRepo(WeatherRepo):
    def __init__(self) -> None:
        self.conn = None
        self._get_db_connection()

    def _get_db_connection(self) -> None:
        self.conn = psycopg2.connect(
            host=db_config.host,
            database='weather',
            user=db_config.username,
            password=db_config.password,
            cursor_factory=RealDictCursor
        )

    def insert_weather_by_city_data(
            self,
            city: str,
            temperature: float,
            feels_like: float,
            pressure: int,
            humidity: int,
            wind_speed: float,
            ) -> None:

        self._get_db_connection()
        cursor = self.conn.cursor()

        insert_query = """
        INSERT INTO weather_by_city (city, temperature, feels_like, pressure, humidity, wind_speed, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            city,
            temperature,
            feels_like,
            pressure,
            humidity,
            wind_speed,
            datetime.now()
            ))

        self.conn.commit()

        cursor.close()
        self.conn.close()

    def read_last_data_by_city(self, city: str) -> Weather | None:
        self._get_db_connection()
        cursor = self.conn.cursor()

        select_query = """
        SELECT * FROM weather_by_city
        WHERE city = %s
        ORDER BY created_at DESC
        LIMIT 1
        """

        cursor.execute(select_query, (city,))

        result = cursor.fetchone()

        cursor.close()
        self.conn.close()

        if not result:
            return None

        datetime_last_request = result['created_at']
        if datetime.now() - datetime_last_request < timedelta(hours=1):
            weather_info = Weather(
                city=result['city'],
                temperature=result['temperature'],
                feels_like=result['feels_like'],
                pressure=result['pressure'],
                humidity=result['humidity'],
                wind_speed=result['wind_speed']
            )
            return weather_info


def get_weather_psyco_repo() -> WeatherPsycoRepo:
    return WeatherPsycoRepo()
