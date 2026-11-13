"""Unit tests that run in CI without docker or certificates.

The Bruno collections (component and integration tests) come later and live in
docs/. These are just a quick safety net so CI catches broken code.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_encounters_not_implemented():
    response = client.get("/encounters")
    assert response.status_code == 501
