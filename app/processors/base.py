from dataclasses import dataclass
from typing import Any, Protocol
@dataclass(frozen=True)
class ProcessorResult:
    status: str
    processor_transaction_id: str | None = None
    card_brand: str | None = None
    card_last_four: str | None = None
    requires_action: bool = False
    next_action_type: str | None = None
    failure_code: str | None = None
    failure_message_safe: str | None = None
    metadata: dict[str, Any] | None = None
class PaymentProcessor(Protocol):
    name: str
    def charge(self, amount:int, currency:str, payment_method_id:str, metadata:dict[str,Any]|None=None) -> ProcessorResult: ...
    def validate_key(self) -> dict[str, Any]: ...
