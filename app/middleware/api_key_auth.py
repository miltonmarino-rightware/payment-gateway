from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session
from app.core.errors import AppError
from app.db.database import get_db
from app.db.models.api_key import ApiKey
from app.services.api_key_service import ApiKeyService

def require_api_key(request: Request, x_api_key: str | None = Header(default=None, alias="X-API-KEY"), db: Session = Depends(get_db)) -> ApiKey:
    if not x_api_key:
        raise AppError("missing_api_key", "Missing X-API-KEY header.", 401)
    api_key = ApiKeyService(db).authenticate(x_api_key)
    if not api_key:
        from app.services.security_service import SecurityService
        SecurityService(db).record_failed_attempt(
            reason="invalid_api_key",
            ip_address=getattr(request.state, 'client_ip', None) if hasattr(request, 'state') else None
        )
        raise AppError("invalid_api_key", "Invalid or inactive API key.", 401)
    return api_key
