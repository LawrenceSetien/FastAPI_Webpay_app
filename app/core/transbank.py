import sys
import logging
import httpx
from typing import Dict, Any
from dataclasses import dataclass
from app.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

@dataclass
class TransactionResponse:
    """Response object for transaction creation to maintain compatibility with SDK response"""
    token: str
    url: str

@dataclass
class CommitResponse:
    """Response object for transaction commit to maintain compatibility with SDK response"""
    amount: float
    status: str
    buy_order: str
    session_id: str
    card_number: str = None
    accounting_date: str = None
    transaction_date: str = None
    authorization_code: str = None
    payment_type_code: str = None
    response_code: int = None
    installments_number: int = None

def get_base_url() -> str:
    """Get the appropriate base URL based on environment"""
    if settings.TRANSBANK_ENVIRONMENT.upper() == "PRODUCTION":
        return "https://webpay3g.transbank.cl"
    else:
        return "https://webpay3gint.transbank.cl"

def get_headers() -> Dict[str, str]:
    """Get authentication headers for Transbank API"""
    return {
        "Tbk-Api-Key-Id": settings.TRANSBANK_COMMERCE_CODE,
        "Tbk-Api-Key-Secret": settings.TRANSBANK_API_KEY,
        "Content-Type": "application/json"
    }

async def create_transaction(amount: float, buy_order: str, session_id: str, return_url: str) -> TransactionResponse:
    """
    Create a new transaction in Transbank using REST API
    """

    base_url = get_base_url()
    headers = get_headers()

    # Prepare request payload
    payload = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": int(amount),  # Transbank expects amount as integer (cents/pesos)
        "return_url": return_url
    }

    url = f"{base_url}/rswebpaytransaction/api/webpay/v1.2/transactions"

    logger.info(f"Creating transaction with payload={payload}")
    logger.info(f"URL: {url}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Transaction created successfully: token={data.get('token')}, url={data.get('url')}")

            return TransactionResponse(
                token=data["token"],
                url=data["url"]
            )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error creating transaction: {e.response.status_code} - {e.response.text}")
        raise Exception(f"Transbank API error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        raise

async def commit_transaction(token: str) -> CommitResponse:
    """
    Commit a transaction using its token via REST API
    """
    logger.info(f"Committing transaction with token={token}")

    base_url = get_base_url()
    headers = get_headers()

    url = f"{base_url}/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Transaction committed successfully: status={data.get('status')}, amount={data.get('amount')}")

            return CommitResponse(
                amount=float(data.get("amount", 0)),
                status=data.get("status", ""),
                buy_order=data.get("buy_order", ""),
                session_id=data.get("session_id", ""),
                card_number=data.get("card_detail", {}).get("card_number", "") if data.get("card_detail") else "",
                accounting_date=data.get("accounting_date", ""),
                transaction_date=data.get("transaction_date", ""),
                authorization_code=data.get("authorization_code", ""),
                payment_type_code=data.get("payment_type_code", ""),
                response_code=data.get("response_code", 0),
                installments_number=data.get("installments_number", 0)
            )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error committing transaction: {e.response.status_code} - {e.response.text}")
        raise Exception(f"Transbank API error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Error committing transaction: {str(e)}")
        raise