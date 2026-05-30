from typing import Any, Literal
from pydantic import BaseModel, Field
class ChargeRequest(BaseModel):
    amount: int = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    processor: Literal["mock", "stripe"] = "mock"
    payment_method_id: str = Field(min_length=3, max_length=255)
    metadata: dict[str, Any] | None = None
class ChargeResponse(BaseModel):
    transaction_id: str
    reference: str
    status: str
    amount: int
    currency: str
    processor: str
    requires_action: bool = False
    next_action_type: str | None = None
    failure_code: str | None = None
    failure_message_safe: str | None = None
