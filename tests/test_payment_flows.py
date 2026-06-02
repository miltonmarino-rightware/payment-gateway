import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, create_all_tables
from app.services.api_key_service import ApiKeyService

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    create_all_tables()
    yield

@pytest.fixture
def api_key():
    db = SessionLocal()
    # Note: Since we protected the endpoint, we need an initial key or a way to create one.
    # For testing, we'll bypass the route and use the service.
    service = ApiKeyService(db)
    key_row, generated = service.create("Test Merchant")
    db.close()
    return generated.plain

def test_charge_success(api_key):
    response = client.post(
        "/api/v1/payments/charge",
        headers={"X-API-KEY": api_key, "Idempotency-Key": "test-success-1"},
        json={
            "amount": 1000,
            "currency": "USD",
            "processor": "mock",
            "payment_method_id": "pm_mock_success"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "succeeded"

def test_charge_decline(api_key):
    response = client.post(
        "/api/v1/payments/charge",
        headers={"X-API-KEY": api_key, "Idempotency-Key": "test-decline-1"},
        json={
            "amount": 1000,
            "currency": "USD",
            "processor": "mock",
            "payment_method_id": "pm_mock_decline"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert response.json()["failure_code"] == "card_declined"

def test_charge_3ds(api_key):
    response = client.post(
        "/api/v1/payments/charge",
        headers={"X-API-KEY": api_key, "Idempotency-Key": "test-3ds-1"},
        json={
            "amount": 1000,
            "currency": "USD",
            "processor": "mock",
            "payment_method_id": "pm_mock_3ds"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "requires_action"
    assert response.json()["requires_action"] is True

def test_idempotency_replay(api_key):
    payload = {
        "amount": 1000,
        "currency": "USD",
        "processor": "mock",
        "payment_method_id": "pm_mock_success"
    }
    headers = {"X-API-KEY": api_key, "Idempotency-Key": "idem-1"}
    
    # First request
    resp1 = client.post("/api/v1/payments/charge", headers=headers, json=payload)
    assert resp1.status_code == 200
    
    # Replay
    resp2 = client.post("/api/v1/payments/charge", headers=headers, json=payload)
    assert resp2.status_code == 200
    assert resp1.json() == resp2.json()

def test_idempotency_conflict(api_key):
    headers = {"X-API-KEY": api_key, "Idempotency-Key": "idem-conflict"}
    
    # First request
    client.post("/api/v1/payments/charge", headers=headers, json={
        "amount": 1000, "currency": "USD", "processor": "mock", "payment_method_id": "pm_mock_success"
    })
    
    # Conflict request (same key, different amount)
    response = client.post("/api/v1/payments/charge", headers=headers, json={
        "amount": 2000, "currency": "USD", "processor": "mock", "payment_method_id": "pm_mock_success"
    })
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "idempotency_conflict"
