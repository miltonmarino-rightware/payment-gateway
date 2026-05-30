from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.core.errors import AppError
from app.db.database import get_db
from app.db.models.api_key import ApiKey
from app.services.api_key_service import ApiKeyService

def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-KEY"), db: Session = Depends(get_db)) -> ApiKey:
    if not x_api_key:
        raise AppError("missing_api_key", "Missing X-API-KEY header.", 401)
    api_key = ApiKeyService(db).authenticate(x_api_key)
    if not api_key:
        raise AppError("invalid_api_key", "Invalid or inactive API key.", 401)
    return api_key
