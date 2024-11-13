from sqlalchemy import BigInteger, DateTime, Float, Integer, String
from sqlalchemy import Column, MetaData, Table

medatadata_obj = MetaData()

weather_by_city_table = Table(
    'weather_by_city',
    medatadata_obj,
    Column('id', BigInteger, primary_key=True),
    Column('city', String),
    Column('temperature', Float),
    Column('feels_like', Float),
    Column('pressure', Integer),
    Column('humidity', Integer),
    Column('wind_speed', Float),
    Column('created_at', DateTime)
)
