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


def test_list_monsters_has_name_and_image():
    response = client.get("/monsters")
    assert response.status_code == 200
    for monster in response.json():
        assert monster["name"]
        assert monster["image_url"]


def test_get_unknown_monster_is_404():
    response = client.get("/monsters/does-not-exist")
    assert response.status_code == 404


def test_get_monster_rejects_bad_id():
    response = client.get("/monsters/BAD_ID!")
    assert response.status_code in (400, 422)
