"""Pytest suite for the synthetic healthz endpoint."""
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_healthz_returns_200():
    response = client.get("/api/v1/healthz")
    assert response.status_code == 200


def test_healthz_body_matches_contract():
    response = client.get("/api/v1/healthz")
    body = response.json()
    assert body == {"status": "ok", "version": "0.1.0"}


def test_healthz_content_type_is_json():
    response = client.get("/api/v1/healthz")
    assert response.headers["content-type"].startswith("application/json")


def test_healthz_is_idempotent_and_side_effect_free():
    first = client.get("/api/v1/healthz").json()
    second = client.get("/api/v1/healthz").json()
    third = client.get("/api/v1/healthz").json()
    assert first == second == third