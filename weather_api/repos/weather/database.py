from datetime import datetime, timedelta

from sqlalchemy import Engine
from sqlalchemy import create_engine, desc, insert, select

from weather_api.config import DATABASE_URL_PSYCOPG
from weather_api.models import weather_by_city_table
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather


class WeatherAlchemyRepo(WeatherRepo):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def insert_weather_by_city_data(
            self,
            city: str,
            tmp: float,
            feels_like: float,
            pressure: int,
            humidity: int,
            wind_speed: float
            ) -> None:
        with self.engine.connect() as conn:
            stmt = insert(weather_by_city_table).values(
                city=city.lower(),
                temperature=tmp,
                feels_like=feels_like,
                pressure=pressure,
                humidity=humidity,
                wind_speed=wind_speed,
                created_at=datetime.now()
            )

            conn.execute(stmt)
            conn.commit()

    def read_last_data_by_city(self, city: str) -> Weather | None:
        with self.engine.connect() as conn:
            query = select(weather_by_city_table).where(
                    weather_by_city_table.c.city == city.lower()
                ).order_by(
                    desc(weather_by_city_table.c.created_at)
                ).limit(1)

            result = conn.execute(query).fetchone()

            if not result:
                return None

            datetime_last_request = result[-1]
            if datetime.now() - datetime_last_request < timedelta(hours=1):
                weather_info = Weather(
                    city=result[1],
                    temperature=result[2],
                    feels_like=result[3],
                    pressure=result[4],
                    humidity=result[5],
                    wind_speed=result[6]
                )
                return weather_info


def get_weather_alchemy_repo() -> WeatherAlchemyRepo:
    engine = create_engine(
        url=DATABASE_URL_PSYCOPG,
        echo=True,
        client_encoding='utf8',
    )
    return WeatherAlchemyRepo(engine)
