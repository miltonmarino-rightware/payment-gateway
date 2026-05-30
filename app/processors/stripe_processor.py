from app.core.config import get_settings
from app.core.errors import AppError
class StripeProcessor:
    name="stripe"
    def __init__(self): self.settings=get_settings()
    def charge(self, amount:int, currency:str, payment_method_id:str, metadata:dict|None=None):
        if not self.settings.stripe_configured:
            raise AppError("processor_not_configured", "Stripe is not configured yet.", 400)
        raise AppError("stripe_not_implemented", "Stripe live charge is reserved for Phase 2B.", 501)
    def validate_key(self)->dict:
        if not self.settings.stripe_configured:
            return {"valid": False, "processor": self.name, "mode": "unknown", "status": "not_configured"}
        return {"valid": True, "processor": self.name, "mode": "configured", "status": "configured"}
