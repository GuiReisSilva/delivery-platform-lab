from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_release_flow():
    r = client.post("/release", json={"service": "api", "version": "1.0.0"})
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "done"

    r2 = client.get("/releases")
    assert r2.status_code == 200
    items = r2.json()["items"]
    assert len(items) >= 1
    assert items[0]["service"] == "api"


def test_live():
    r = client.get("/live")
    assert r.status_code == 200
    assert r.json()["status"] == "alive"


def test_ready():
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_metrics():
    client.post("/release", json={"service": "api", "version": "1.0.0"})

    r = client.get("/metrics")
    assert r.status_code == 200
    assert "text/plain" in r.headers["content-type"]

    body = r.text
    assert "release_requests_total" in body
    assert 'service="api"' in body
    assert "release_duration_seconds" in body
