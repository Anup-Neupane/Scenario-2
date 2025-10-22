import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_hello_route(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Hello from Simple App!"
    assert "version" in data


def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_info_route(client):
    response = client.get('/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data["app"] == "Simple Python App"
    assert data["language"] == "Python"
