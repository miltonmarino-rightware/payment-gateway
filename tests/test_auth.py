import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.api_key_service import ApiKeyService
from app.db.database import SessionLocal

client = TestClient(app)

@pytest.fixture
def initial_api_key():
    db = SessionLocal()
    service = ApiKeyService(db)
    key_row, generated = service.create("Master Key")
    db.close()
    return generated.plain

def test_unauthorized_access():
    response = client.get("/api/v1/api-keys")
    assert response.status_code == 401

def test_authorized_list_keys(initial_api_key):
    response = client.get("/api/v1/api-keys", headers={"X-API-KEY": initial_api_key})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_key_protected(initial_api_key):
    # Test that creating a key now requires an existing key
    response = client.post(
        "/api/v1/api-keys",
        headers={"X-API-KEY": initial_api_key},
        json={"name": "New Merchant", "processor_scope": "mock"}
    )
    assert response.status_code == 200
    assert "api_key" in response.json()

def test_invalid_api_key():
    response = client.get("/api/v1/api-keys", headers={"X-API-KEY": "invalid_key"})
    assert response.status_code == 401
