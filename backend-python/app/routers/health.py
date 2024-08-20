# app/routers/health.py
from fastapi import APIRouter
from app.eth_client import EthereumClient

router = APIRouter()

@router.get("/health")
def health():
    client = EthereumClient()
    return {"connected": True, "chain_id": client.chain_id}