from datetime import datetime
from sqlalchemy.orm import Session
from app.core.security import GeneratedApiKey, generate_api_key, hash_secret
from app.db.models.api_key import ApiKey
class ApiKeyService:
    def __init__(self, db: Session): self.db=db
    def create(self, name:str, processor_scope:str="mock") -> tuple[ApiKey, GeneratedApiKey]:
        generated=generate_api_key(); row=ApiKey(name=name, prefix=generated.prefix, key_hash=generated.key_hash, processor_scope=processor_scope, is_active=True)
        self.db.add(row); self.db.commit(); self.db.refresh(row); return row, generated
    def authenticate(self, plain_key:str) -> ApiKey | None:
        row=self.db.query(ApiKey).filter(ApiKey.key_hash==hash_secret(plain_key), ApiKey.is_active == True).first()  # noqa
        if row: row.last_used_at=datetime.utcnow(); self.db.commit()
        return row
    def list(self)->list[ApiKey]: return self.db.query(ApiKey).order_by(ApiKey.created_at.desc()).all()
