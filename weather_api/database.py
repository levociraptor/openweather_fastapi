import psycopg2
import sqlalchemy as db
from sqlalchemy import create_engine, insert

from datetime import datetime

from psycopg2.extras import RealDictCursor
from weather_api.config import db_config, DATABASE_URL_PSYCOPG
from weather_api.models import medatadata_obj, weather_by_city_table


def get_db_connection():
    conn = psycopg2.connect(
        host=db_config.host,
        database='weather',
        user=db_config.username,
        password=db_config.password,
        cursor_factory=RealDictCursor
    )

    return conn


def insert_weather_by_city_data(
        city,
        temperature,
        feels_like,
        pressure,
        humidity,
        wind_speed,
        datetime):

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO weather_by_city (city, temperature, feels_like, pressure, humidity, wind_speed, datetime)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (
        city,
        temperature,
        feels_like,
        pressure,
        humidity,
        wind_speed,
        datetime
        ))

    conn.commit()

    cursor.close()
    conn.close()


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
            datetime=datetime.now()
            )

        conn.execute(stmt)
        conn.commit()
