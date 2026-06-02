from sqlalchemy.orm import Session
from app.db.models.failed_attempt import FailedAttempt

class SecurityService:
    def __init__(self, db: Session):
        self.db = db

    def record_failed_attempt(self, reason: str, api_key_id: str | None = None, ip_address: str | None = None):
        """
        Record a failed access or payment attempt for security monitoring.
        """
        attempt = FailedAttempt(
            reason=reason,
            api_key_id=api_key_id,
            ip_address=ip_address
        )
        self.db.add(attempt)
        self.db.commit()
