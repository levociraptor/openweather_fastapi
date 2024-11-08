from datetime import datetime, timezone

from sqlalchemy import MetaData, text, String, Table, Column, BigInteger, Float, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

medatadata_obj = MetaData()


class Base(DeclarativeBase):
    pass


# class Weather_by_city(Base):
#     __tablename__ = 'weather_by_city'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     city: Mapped[str] = mapped_column(String(70))
#     temperature: Mapped[float]
#     feels_like: Mapped[float]
#     pressure: Mapped[int]
#     humidity: Mapped[int]
#     wind_speed: Mapped[float]
#     created_at: Mapped[datetime]


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