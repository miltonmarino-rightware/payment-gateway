from datetime import datetime
from pydantic import BaseModel, ConfigDict
class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    reference: str
    amount: int
    currency: str
    status: str
    processor: str
    processor_transaction_id: str | None = None
    card_brand: str | None = None
    card_last_four: str | None = None
    failure_code: str | None = None
    failure_message_safe: str | None = None
    requires_action: bool
    next_action_type: str | None = None
    created_at: datetime
