import pytest
from fastapi.testclient import TestClient
from space import app, Planet_body

client = TestClient(app)

def test_current_constel():
    response = client.get("/api/constellation/current")
    assert response.status_code == 200

    data = response.json()
    assert data["body"] in Planet_body.keys()
    assert "constellation_code" in data
    assert "constellation_name" in data


def test_post_empty_data():
    response = client.post("/api/calculation")
    assert response.status_code == 422 


def test_post_valid_data():
    response = client.post("/api/calculation", json = {'time_data': '2026/09/16 12:00:00', 'lat': 55.75, 'lon': 37.61})
    assert response.status_code == 200

def test_post_invalid_data():
    response = client.post("/api/calculation", json = {'time_data': 2026, 'lat': 55.75, 'lon': 37.61})
    assert response.status_code == 422



