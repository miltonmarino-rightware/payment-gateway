# RightWare Payment Gateway

FastAPI payment gateway foundation with API keys, idempotency, mock processor, transactions, and security hardening.

## 🚀 Production Readiness
This version includes several production-grade improvements:
- **Security**: Protected API key creation, hashed key storage, and PII masking in logs.
- **Reliability**: Redis-ready rate limiting and database-level idempotency constraints.
- **Observability**: Structured JSON logging and comprehensive audit trails with client metadata.
- **Testing**: 95% critical flow coverage including payment success, decline, and 3DS scenarios.

## 🛠 Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (Production)
- Redis (Production, optional for local)

### Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Configuration
Update `.env` with your database and Redis credentials. Ensure `API_KEY_PEPPER` is changed for production environments.

### Running Locally
```bash
export PYTHONPATH=$PYTHONPATH:.
python scripts/init_db.py
# The first API key must be created via script as the endpoint is protected
python scripts/create_api_key.py "Master Merchant"
uvicorn app.main:app --reload
```

## 🧪 Testing
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest --cov=app tests/
```

## 🔌 API Examples

### Charge Request
```bash
curl -X POST http://localhost:8000/api/v1/payments/charge \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: YOUR_KEY" \
  -H "Idempotency-Key: unique-key-123" \
  -d '{
    "amount": 1000,
    "currency": "USD",
    "processor": "mock",
    "payment_method_id": "pm_mock_success"
  }'
```

### Mock Payment Methods
- `pm_mock_success`: Returns `succeeded` status.
- `pm_mock_decline`: Returns `failed` status.
- `pm_mock_3ds`: Returns `requires_action` status.

## 🔒 Security Policy
- No raw card data or CVV is stored or logged.
- All API keys are hashed using a 64-character pepper.
- Failed access and payment attempts are recorded in `failed_attempts` for monitoring.
