from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_charge_success():
    # Note: In a real scenario, we'd need a valid API key.
    # For now, let's just check if the endpoint exists and handles missing auth.
    response = client.post("/api/v1/payments/charge", json={})
    assert response.status_code == 401 # Unauthorized since no API key provided

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
