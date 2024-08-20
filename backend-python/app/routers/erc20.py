import json
from fastapi import APIRouter, HTTPException
from app.eth_client import EthereumClient
from app.logic.entities import DeployRequest

router = APIRouter()

# Carica ABI + bytecode da JSON
with open("contracts/ERC20.json") as f:
    artifact = json.load(f)
ERC20_ABI = artifact["abi"]
ERC20_BYTECODE = artifact["bytecode"]

@router.post("/erc20/deploy")
def deploy_erc20(req: DeployRequest):
    client = EthereumClient()
    try:
        addr = client.deploy_contract(
            abi=ERC20_ABI,
            bytecode=ERC20_BYTECODE,
            constructor_args=(req.name, req.symbol, req.total_supply)
        )
        return {"contract_address": addr}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))