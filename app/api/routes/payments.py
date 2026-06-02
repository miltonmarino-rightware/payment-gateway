from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from app.core.errors import AppError
from app.db.database import get_db
from app.db.models.transaction import Transaction
from app.middleware.api_key_auth import require_api_key
from app.middleware.rate_limit import check_rate_limit
from app.schemas.charge import ChargeRequest, ChargeResponse
from app.schemas.transaction import TransactionResponse
from app.services.audit_service import AuditService
from app.services.idempotency_service import IdempotencyService, request_hash
from app.services.payment_service import PaymentService
router=APIRouter(prefix="/api/v1/payments", tags=["payments"])
@router.post("/charge", response_model=ChargeResponse)
def charge(payload:ChargeRequest, request:Request, db:Session=Depends(get_db), api_key=Depends(require_api_key), idempotency_key:str|None=Header(default=None, alias="Idempotency-Key")):
    check_rate_limit(request, api_key.id)
    if not idempotency_key: raise AppError("missing_idempotency_key", "Missing Idempotency-Key header.", 400)
    payload_hash=request_hash(payload.model_dump()); idem=IdempotencyService(db)
    existing=idem.get_existing(api_key.id, idempotency_key, payload_hash)
    if existing: return existing.response_body
    response=PaymentService(db).charge(payload); body=response.model_dump()
    idem.store(api_key.id, idempotency_key, payload_hash, body, 200, response.transaction_id)
    ip_address = getattr(request.state, 'client_ip', None)
    user_agent = getattr(request.state, 'user_agent', None)
    AuditService(db).record("charge_created", "transaction", response.transaction_id, api_key.id, {"status": response.status}, ip_address, user_agent)
    return response
@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id:str, db:Session=Depends(get_db), _api_key=Depends(require_api_key)):
    txn=db.query(Transaction).filter(Transaction.id==transaction_id).first()
    if not txn: raise AppError("transaction_not_found", "Transaction not found.", 404)
    return txn
@router.get("/{transaction_id}/status")
def get_transaction_status(transaction_id:str, db:Session=Depends(get_db), _api_key=Depends(require_api_key)):
    txn=db.query(Transaction).filter(Transaction.id==transaction_id).first()
    if not txn: raise AppError("transaction_not_found", "Transaction not found.", 404)
    return {"transaction_id":txn.id,"status":txn.status}
