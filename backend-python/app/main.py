# app/main.py
from fastapi import FastAPI
from app.routers import health, erc20

app = FastAPI(title="Ethereum Microservice")

app.include_router(health.router, prefix="/api")
# app.include_router(erc20.router, prefix="/api")