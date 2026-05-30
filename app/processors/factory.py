from app.core.errors import AppError
from app.processors.mock_processor import MockProcessor
from app.processors.stripe_processor import StripeProcessor
def get_processor(name:str):
    if name=="mock": return MockProcessor()
    if name=="stripe": return StripeProcessor()
    raise AppError("unsupported_processor", "Unsupported payment processor.", 400)
