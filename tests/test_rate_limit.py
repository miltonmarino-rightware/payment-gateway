import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.api_key_service import ApiKeyService
from app.db.database import SessionLocal
from app.core.config import get_settings

client = TestClient(app)

@pytest.fixture
def api_key():
    db = SessionLocal()
    service = ApiKeyService(db)
    key_row, generated = service.create("Rate Limit Merchant")
    db.close()
    return generated.plain

def test_rate_limiting(api_key):
    settings = get_settings()
    limit = settings.rate_limit_requests
    
    # Make requests up to the limit
    # Using transaction retrieval as it's a GET route with auth
    for i in range(limit):
        response = client.get("/api/v1/payments/non-existent", headers={"X-API-KEY": api_key})
        # We expect 404 but rate limit should still increment
        assert response.status_code in [200, 404]
    
    # Next request should be rate limited
    response = client.get("/api/v1/payments/non-existent", headers={"X-API-KEY": api_key})
    assert response.status_code == 429
    assert response.json()["error"]["code"] == "rate_limit_exceeded"
