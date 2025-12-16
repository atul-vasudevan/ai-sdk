from fastapi.testclient import TestClient
from service.app.main import app


def test_rejects_empty():
    client = TestClient(app)
    r = client.post("/summarise", json={"text": " "})
    assert r.status_code in (400, 422)


def test_rejects_too_large():
    client = TestClient(app)
    r = client.post("/summarise", json={"text": "a" * 13000})
    assert r.status_code in (400, 422)
