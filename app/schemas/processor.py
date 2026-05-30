from pydantic import BaseModel
class ValidateProcessorRequest(BaseModel):
    processor: str = "mock"
class ValidateProcessorResponse(BaseModel):
    valid: bool
    processor: str
    mode: str
    status: str
