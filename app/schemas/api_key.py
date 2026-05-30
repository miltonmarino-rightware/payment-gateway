from datetime import datetime
from pydantic import BaseModel, ConfigDict
class CreateApiKeyRequest(BaseModel):
    name: str
    processor_scope: str = "mock"
class CreateApiKeyResponse(BaseModel):
    id: str
    name: str
    prefix: str
    api_key: str
class ApiKeyListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    prefix: str
    processor_scope: str
    is_active: bool
    created_at: datetime
