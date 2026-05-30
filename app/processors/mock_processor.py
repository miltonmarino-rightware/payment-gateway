from app.processors.base import ProcessorResult
class MockProcessor:
    name="mock"
    def charge(self, amount:int, currency:str, payment_method_id:str, metadata:dict|None=None)->ProcessorResult:
        if payment_method_id=="pm_mock_decline":
            return ProcessorResult(status="failed", failure_code="card_declined", failure_message_safe="Payment was declined.", card_brand="visa", card_last_four="0002")
        if payment_method_id=="pm_mock_3ds":
            return ProcessorResult(status="requires_action", requires_action=True, next_action_type="redirect", card_brand="visa", card_last_four="3184")
        return ProcessorResult(status="succeeded", processor_transaction_id="mock_txn_success", card_brand="visa", card_last_four="4242")
    def validate_key(self)->dict:
        return {"valid": True, "processor": self.name, "mode": "sandbox", "status": "configured"}
