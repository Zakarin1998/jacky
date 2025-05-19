from pydantic import BaseModel

class TransferRequest(BaseModel):
    to: str
    amount_eth: float
