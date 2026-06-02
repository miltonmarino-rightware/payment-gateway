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
    service = ApiKeyService(db)
    key_row, generated = service.create("Retrieval Test Merchant")
    db.close()
    return generated.plain

def test_transaction_retrieval_flow(api_key):
    # 1. Create a charge
    charge_resp = client.post(
        "/api/v1/payments/charge",
        headers={"X-API-KEY": api_key, "Idempotency-Key": "retrieval-1"},
        json={
            "amount": 5000,
            "currency": "USD",
            "processor": "mock",
            "payment_method_id": "pm_mock_success"
        }
    )
    assert charge_resp.status_code == 200
    txn_id = charge_resp.json()["transaction_id"]
    
    # 2. Retrieve the transaction
    get_resp = client.get(
        f"/api/v1/payments/{txn_id}",
        headers={"X-API-KEY": api_key}
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == txn_id
    assert get_resp.json()["amount"] == 5000
    
    # 3. Retrieve status only
    status_resp = client.get(
        f"/api/v1/payments/{txn_id}/status",
        headers={"X-API-KEY": api_key}
    )
    assert status_resp.status_code == 200
    assert status_resp.json()["status"] == "succeeded"

def test_retrieve_non_existent_transaction(api_key):
    response = client.get(
        "/api/v1/payments/non-existent-id",
        headers={"X-API-KEY": api_key}
    )
    assert response.status_code == 404
