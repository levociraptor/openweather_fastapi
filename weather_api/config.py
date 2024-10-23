from dotenv import load_dotenv

from dataclasses import dataclass
import os


@dataclass
class Config:
    url: str
    api_key: str


load_dotenv()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv('API_KEY')

congig = Config(BASE_URL, API_KEY)
