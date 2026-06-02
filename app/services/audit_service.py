from sqlalchemy.orm import Session
from app.db.models.audit_log import AuditLog

class AuditService:
    def __init__(self, db: Session): 
        self.db = db
    
    def record(self, action: str, resource_type: str, resource_id: str | None = None, actor_api_key_id: str | None = None, metadata: dict | None = None, ip_address: str | None = None, user_agent: str | None = None):
        self.db.add(AuditLog(
            action=action, 
            resource_type=resource_type, 
            resource_id=resource_id, 
            actor_api_key_id=actor_api_key_id, 
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_json=metadata
        ))
        self.db.commit()
