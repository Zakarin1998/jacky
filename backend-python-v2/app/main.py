from fastapi import FastAPI
from routers.eth_router import router as eth_router

TITLE = "Ethereum Service Based on web3 library."
app = FastAPI(title=TITLE)

# Routers
app.include_router(eth_router, prefix="/eth", tags=["eth"])
