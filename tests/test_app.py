from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK