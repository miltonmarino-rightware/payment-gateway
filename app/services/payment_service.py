from uuid import uuid4
from sqlalchemy.orm import Session
from app.db.models.transaction import Transaction
from app.processors.factory import get_processor
from app.schemas.charge import ChargeRequest, ChargeResponse
class PaymentService:
    def __init__(self, db:Session): self.db=db
    def charge(self, payload:ChargeRequest)->ChargeResponse:
        processor=get_processor(payload.processor); reference=f"rw_{uuid4().hex[:18]}"
        txn=Transaction(reference=reference, amount=payload.amount, currency=payload.currency.upper(), status="processing", processor=payload.processor, payment_method_id=payload.payment_method_id, metadata_json=payload.metadata)
        self.db.add(txn); self.db.flush()
        result=processor.charge(payload.amount, payload.currency.upper(), payload.payment_method_id, payload.metadata)
        txn.status=result.status; txn.processor_transaction_id=result.processor_transaction_id; txn.card_brand=result.card_brand; txn.card_last_four=result.card_last_four; txn.failure_code=result.failure_code; txn.failure_message_safe=result.failure_message_safe; txn.requires_action=result.requires_action; txn.next_action_type=result.next_action_type
        
        if txn.status == "failed":
            from app.services.security_service import SecurityService
            SecurityService(self.db).record_failed_attempt(
                reason=f"payment_failed: {txn.failure_code}",
                api_key_id=None # We'd need to pass this in if we wanted to track per merchant
            )
            
        self.db.commit(); self.db.refresh(txn)
        return ChargeResponse(transaction_id=txn.id, reference=txn.reference, status=txn.status, amount=txn.amount, currency=txn.currency, processor=txn.processor, requires_action=txn.requires_action, next_action_type=txn.next_action_type, failure_code=txn.failure_code, failure_message_safe=txn.failure_message_safe)
