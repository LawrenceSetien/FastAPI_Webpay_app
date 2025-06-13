from fastapi import APIRouter, HTTPException
from app.schemas.payment import PaymentRequest, PaymentResponse, PaymentStatus
from app.core.transbank import create_transaction, commit_transaction

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create", response_model=PaymentResponse)
async def create_payment(payment: PaymentRequest):
    """
    Create a new payment transaction
    """
    try:
        response = await create_transaction(
            amount=payment.amount,
            buy_order=payment.buy_order,
            session_id=payment.session_id,
            return_url=payment.return_url
        )
        return PaymentResponse(
            token=response.token,
            url=response.url
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/confirm", response_model=PaymentStatus)
async def confirm_payment(token: str):
    """
    Confirm a payment transaction using its token
    """
    try:
        response = await commit_transaction(token)
        return PaymentStatus(
            amount=response.amount,
            status=response.status,
            buy_order=response.buy_order,
            session_id=response.session_id,
            card_number=response.card_number,
            accounting_date=response.accounting_date,
            transaction_date=response.transaction_date
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))