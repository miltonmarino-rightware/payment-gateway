import hashlib, json
from sqlalchemy.orm import Session
from app.core.errors import AppError
from app.db.models.idempotency_key import IdempotencyKey
def request_hash(payload:dict)->str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
class IdempotencyService:
    def __init__(self, db:Session): self.db=db
    def get_existing(self, api_key_id:str, key:str, payload_hash:str):
        row=self.db.query(IdempotencyKey).filter(IdempotencyKey.api_key_id==api_key_id, IdempotencyKey.idempotency_key==key).first()
        if row and row.request_hash != payload_hash:
            raise AppError("idempotency_conflict", "Same Idempotency-Key used with different payload.", 409)
        return row
    def store(self, api_key_id:str, key:str, payload_hash:str, response_body:dict, status_code:int, transaction_id:str|None):
        self.db.add(IdempotencyKey(api_key_id=api_key_id, idempotency_key=key, request_hash=payload_hash, response_body=response_body, status_code=status_code, transaction_id=transaction_id)); self.db.commit()
