# RightWare Payment Gateway

FastAPI payment gateway foundation with API keys, idempotency, mock processor, transactions and Stripe placeholder.

## Local run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Note: Ensure PYTHONPATH includes the current directory
export PYTHONPATH=$PYTHONPATH:.

python scripts/init_db.py
python scripts/create_api_key.py "Test Merchant"
uvicorn app.main:app --reload
```

## Charge test

```bash
curl -X POST http://localhost:8000/api/v1/payments/charge \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: YOUR_KEY" \
  -H "Idempotency-Key: test-001" \
  -d '{"amount":1000,"currency":"USD","processor":"mock","payment_method_id":"pm_mock_success"}'
```

Mock methods: `pm_mock_success`, `pm_mock_decline`, `pm_mock_3ds`.
