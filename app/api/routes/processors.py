from fastapi import APIRouter, Depends
from app.middleware.api_key_auth import require_api_key
from app.processors.factory import get_processor
from app.schemas.processor import ValidateProcessorRequest, ValidateProcessorResponse
router=APIRouter(prefix="/api/v1/processors", tags=["processors"])
@router.post("/validate-key", response_model=ValidateProcessorResponse)
def validate_processor(payload:ValidateProcessorRequest, _api_key=Depends(require_api_key)):
    return ValidateProcessorResponse(**get_processor(payload.processor).validate_key())
