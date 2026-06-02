from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.middleware.api_key_auth import require_api_key
from app.schemas.api_key import CreateApiKeyRequest, CreateApiKeyResponse, ApiKeyListItem
from app.services.api_key_service import ApiKeyService
router=APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])
@router.post("", response_model=CreateApiKeyResponse)
def create_api_key(payload:CreateApiKeyRequest, db:Session=Depends(get_db), _api_key=Depends(require_api_key)):
    row, generated=ApiKeyService(db).create(payload.name, payload.processor_scope)
    return CreateApiKeyResponse(id=row.id, name=row.name, prefix=row.prefix, api_key=generated.plain)
@router.get("", response_model=list[ApiKeyListItem])
def list_api_keys(db:Session=Depends(get_db), _api_key=Depends(require_api_key)):
    return ApiKeyService(db).list()
