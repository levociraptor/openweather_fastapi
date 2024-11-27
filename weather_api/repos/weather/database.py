from datetime import datetime, timedelta

from sqlalchemy import desc, insert, select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from weather_api.config import DATABASE_URL_PSYCOPG
from weather_api.models import weather_by_city_table
from weather_api.repos.weather.repo import WeatherRepo
from weather_api.schemas import Weather


class WeatherAlchemyRepo(WeatherRepo):
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def insert_weather_by_city_data(
            self,
            city: str,
            tmp: float,
            feels_like: float,
            pressure: float,
            humidity: int,
            wind_speed: float
            ) -> None:
        async with self.engine.connect() as conn:
            stmt = insert(weather_by_city_table).values(
                city=city.lower(),
                temperature=tmp,
                feels_like=feels_like,
                pressure=pressure,
                humidity=humidity,
                wind_speed=wind_speed,
                created_at=datetime.now()
            )

            await conn.execute(stmt)
            await conn.commit()

    async def read_last_data_by_city(self, city: str) -> Weather | None:
        async with self.engine.connect() as conn:
            query = select(weather_by_city_table).where(
                    weather_by_city_table.c.city == city.lower()
                ).order_by(
                    desc(weather_by_city_table.c.created_at)
                ).limit(1)

            result = await conn.execute(query)
            row = result.fetchone()

            if not row:
                return None

            datetime_last_request = row[-1]
            if datetime.now() - datetime_last_request < timedelta(hours=1):
                weather_info = Weather(
                    city=row[1],
                    temperature=row[2],
                    feels_like=row[3],
                    pressure=row[4],
                    humidity=row[5],
                    wind_speed=row[6]
                )
                return weather_info
            return None


def get_weather_alchemy_repo() -> WeatherAlchemyRepo:
    engine = create_async_engine(
        url=DATABASE_URL_PSYCOPG,
        echo=True,
    )
    return WeatherAlchemyRepo(engine)
