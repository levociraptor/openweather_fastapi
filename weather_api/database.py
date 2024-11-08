from sqlalchemy import create_engine, insert, select, desc

from datetime import datetime

from weather_api.config import DATABASE_URL_PSYCOPG
from weather_api.models import weather_by_city_table


engine = create_engine(
    url=DATABASE_URL_PSYCOPG,
    echo=True,
    client_encoding='utf8'
)


def insert_weather_by_city_data_alq(
        city: str,
        tmp: float,
        feels_like: float,
        pressure: int,
        humidity: int,
        wind_speed: float
    ):
    with engine.connect() as conn:
        stmt = insert(weather_by_city_table).values(
            city=city,
            temperature=tmp,
            feels_like=feels_like,
            pressure=pressure,
            humidity=humidity,
            wind_speed=wind_speed,
            created_at=datetime.now()
        )

        conn.execute(stmt)
        conn.commit()


def read_last_data_by_city_alq(city: str):
    with engine.connect() as conn:
        query = select(weather_by_city_table).where(
                weather_by_city_table.c.city == city
            ).order_by(
                desc(weather_by_city_table.c.created_at)
            ).limit(1)

        result = conn.execute(query).fetchone()

        return result
