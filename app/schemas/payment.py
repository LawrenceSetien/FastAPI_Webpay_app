from pydantic import BaseModel, Field
from typing import Optional

class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Payment amount in CLP")
    buy_order: str = Field(..., min_length=1, max_length=26, description="Unique order identifier")
    session_id: str = Field(..., min_length=1, max_length=61, description="Session identifier")
    return_url: str = Field(..., description="URL to return after payment")

class PaymentResponse(BaseModel):
    token: str
    url: str

class PaymentStatus(BaseModel):
    amount: float
    status: str
    buy_order: str
    session_id: str
    card_number: Optional[str] = None
    accounting_date: Optional[str] = None
    transaction_date: Optional[str] = None