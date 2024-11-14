import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class WeatherClientConfig:
    url: str
    api_key: str


@dataclass
class DbConfig:
    host: str
    username: str
    password: str
    db_name: str
    db_port: str


load_dotenv()

BASE_URL_OPENWEATHER = "https://api.openweathermap.org/data/2.5/weather"
API_KEY_OPENWEATHER = os.environ['API_KEY_OPENWEATHER']
openweather_config = WeatherClientConfig(BASE_URL_OPENWEATHER, API_KEY_OPENWEATHER)

BASE_URL_WEATHERSTACK = "https://api.weatherstack.com/current"
API_KEY_WEATHERSTACK = os.environ['API_KEY_WEATHERSTACK']
weatherstack_config = WeatherClientConfig(BASE_URL_WEATHERSTACK, API_KEY_WEATHERSTACK)

BASE_URL_WEATHERBIT = "https://api.weatherbit.io/v2.0/current"
API_KEY_WEATHERBIT = os.environ['API_KEY_WEATHERBIT']
weatherbit_config = WeatherClientConfig(BASE_URL_WEATHERBIT, API_KEY_WEATHERBIT)

HOST = os.environ['HOST']
USERNAME = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
DB_NAME = os.environ['DB_NAME']
DP_PORT = os.environ['DB_PORT']

db_config = DbConfig(HOST, USERNAME, PASSWORD, DB_NAME, DP_PORT)

DATABASE_URL_PSYCOPG = (
    f'postgresql+psycopg://{db_config.username}:{db_config.password}'
    f'@{db_config.host}:{db_config.db_port}/{db_config.db_name}'
    '?client_encoding=utf8'
)
