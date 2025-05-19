from fastapi import APIRouter, HTTPException
from app.schemas.transfer import TransferRequest
from app.clients.eth_client import EthereumClient
from app.config import RPC_URL, PRIVATE_KEY, CHAIN_ID
from app.logging_conf import logger

router = APIRouter()
eth_client = EthereumClient(RPC_URL, PRIVATE_KEY, CHAIN_ID)

@router.get("/health")
def health():
    try:
        info = eth_client.health()
        return {"status": "ok", **info}
    except Exception as e:
        logger.error("Health endpoint error: %s", e)
        raise HTTPException(503, "Ethereum unreachable")

@router.post("/transfer")
def transfer(req: TransferRequest):
    try:
        amount_wei = eth_client.w3.to_wei(req.amount_eth, "ether")
        tx_hash = eth_client.transfer_eth(req.to, amount_wei)
        return {"tx_hash": tx_hash}
    except Exception as e:
        logger.error("Transfer endpoint error: %s", e)
        raise HTTPException(400, str(e))
