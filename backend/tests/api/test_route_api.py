import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # lifespan 실행 -> 그래프 적재
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["nodes"] == 9


def test_safe_route_ok(client):
    r = client.post(
        "/api/v1/routes/safe",
        json={
            "origin": {"lat": 37.5660, "lon": 126.9780},
            "destination": {"lat": 37.5680, "lon": 126.9800},
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["node_count"] >= 2
    assert "X-Process-Time-ms" in r.headers


def test_invalid_coordinate_returns_400(client):
    r = client.post(
        "/api/v1/routes/safe",
        json={
            "origin": {"lat": 999, "lon": 126.9780},
            "destination": {"lat": 37.5680, "lon": 126.9800},
        },
    )
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "INVALID_REQUEST"


def test_far_coordinate_returns_404(client):
    r = client.post(
        "/api/v1/routes/safe",
        json={
            "origin": {"lat": 35.0, "lon": 129.0},
            "destination": {"lat": 37.5680, "lon": 126.9800},
        },
    )
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "NODE_NOT_FOUND"

