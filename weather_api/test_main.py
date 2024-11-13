from fastapi.testclient import TestClient

from .server import app

client = TestClient(app)


def test__url_weather__return_status_code_200():
    url = '/weather/?city=london'

    response = client.get(url)

    assert response.status_code == 200


def test__url_weather__return_error_message_when_city_not_exist():
    url = '/weather/?city=londoasdn'
    error_message = {'Error': 'city not found'}

    response = client.get(url)

    assert response.json() == error_message
