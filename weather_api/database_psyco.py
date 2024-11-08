import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime

from weather_api.config import db_config


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
        ):

    conn = get_db_connection()
    cursor = conn.cursor()

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

    conn.commit()

    cursor.close()
    conn.close()


def read_last_data_by_city(city: str):

    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = """
    SELECT * FROM weather_by_city
    WHERE city = %s
    ORDER BY created_at DESC
    LIMIT 1
    """

    cursor.execute(select_query, (city,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result
