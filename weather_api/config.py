from dotenv import load_dotenv

from dataclasses import dataclass
import os


@dataclass
class Config:
    url: str
    api_key: str

@dataclass
class DbConfig:
    host: str
    username: str
    password: str
    db_name: str
    db_port: int


load_dotenv()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv('API_KEY')

config = Config(BASE_URL, API_KEY)

HOST = os.getenv('HOST')
USERNAME = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DP_PORT = os.getenv('DB_PORT')

db_config = DbConfig(HOST, USERNAME, PASSWORD, DB_NAME, DP_PORT)

DATABASE_URL_PSYCOPG = f'postgresql+psycopg://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.db_port}/{db_config.db_name}?client_encoding=utf8'
