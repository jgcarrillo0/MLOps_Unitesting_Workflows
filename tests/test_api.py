"""Pruebas de endpoints con TestClient (sin servidor externo)."""

import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_clean_text_endpoint(client: TestClient) -> None:
    response = client.post("/clean-text", json={"text": "  HOLA  Mundo "})
    assert response.status_code == 200
    assert response.json() == {"result": "hola mundo"}


def test_transform_feature_endpoint(client: TestClient) -> None:
    payload = {"value": 25, "minimum": 0, "maximum": 100}
    response = client.post("/transform-feature", json=payload)
    assert response.status_code == 200
    assert response.json() == {"result": 0.25}


def test_validate_range_endpoint_error(client: TestClient) -> None:
    payload = {"value": 101, "minimum": 0, "maximum": 100}
    response = client.post("/validate-range", json=payload)
    assert response.status_code == 422
    assert "fuera del rango" in response.json()["detail"]


def test_transform_feature_endpoint_error(client: TestClient) -> None:
    payload = {"value": 5, "minimum": 5, "maximum": 5}
    response = client.post("/transform-feature", json=payload)
    assert response.status_code == 422


def test_api_rechaza_campo_inesperado(client: TestClient) -> None:
    response = client.post("/clean-text", json={"text": "ok", "other": "dato"})
    assert response.status_code == 422
