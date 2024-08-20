from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List

# Database connection and session setup
DATABASE_URL = "sqlite:///./deposit_addresses.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------
# SQLAlchemy Models
# -----------------------------0
class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

class Chain(Base):
    __tablename__ = "chains"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

class WalletType(Base):
    __tablename__ = "wallet_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

class DepositAddress(Base):
    __tablename__ = "deposit_addresses"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, nullable=False)
    chain_id = Column(Integer, nullable=False)
    wallet_type_id = Column(Integer, nullable=False)
    address = Column(Text, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

# Create all tables
Base.metadata.create_all(bind=engine)

# -----------------------------
# Pydantic Schemas
# -----------------------------
class ProviderCreate(BaseModel):
    name: str

class ProviderOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ChainCreate(BaseModel):
    name: str

class ChainOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class WalletTypeCreate(BaseModel):
    name: str

class WalletTypeOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class DepositAddressCreate(BaseModel):
    provider_id: int
    chain_id: int
    wallet_type_id: int
    address: str

class DepositAddressOut(BaseModel):
    id: int
    provider_id: int
    chain_id: int
    wallet_type_id: int
    address: str
    created_at: str
    updated_at: str
    class Config:
        orm_mode = True

# -----------------------------
# Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="Deposit Addresses API")

# ----- Providers Endpoints -----
@app.post("/providers/", response_model=ProviderOut)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    db_provider = Provider(name=provider.name)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

@app.get("/providers/", response_model=List[ProviderOut])
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()

@app.get("/providers/{provider_id}", response_model=ProviderOut)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@app.delete("/providers/{provider_id}", response_model=ProviderOut)
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    db.delete(provider)
    db.commit()
    return provider

# ----- Chains Endpoints -----
@app.post("/chains/", response_model=ChainOut)
def create_chain(chain: ChainCreate, db: Session = Depends(get_db)):
    db_chain = Chain(name=chain.name)
    db.add(db_chain)
    db.commit()
    db.refresh(db_chain)
    return db_chain

@app.get("/chains/", response_model=List[ChainOut])
def list_chains(db: Session = Depends(get_db)):
    return db.query(Chain).all()

@app.get("/chains/{chain_id}", response_model=ChainOut)
def get_chain(chain_id: int, db: Session = Depends(get_db)):
    chain = db.query(Chain).filter(Chain.id == chain_id).first()
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")
    return chain

@app.delete("/chains/{chain_id}", response_model=ChainOut)
def delete_chain(chain_id: int, db: Session = Depends(get_db)):
    chain = db.query(Chain).filter(Chain.id == chain_id).first()
    if not chain:
        raise HTTPException(status_code=404, detail="Chain not found")
    db.delete(chain)
    db.commit()
    return chain

# ----- Wallet Types Endpoints -----
@app.post("/wallet_types/", response_model=WalletTypeOut)
def create_wallet_type(wallet_type: WalletTypeCreate, db: Session = Depends(get_db)):
    db_wallet_type = WalletType(name=wallet_type.name)
    db.add(db_wallet_type)
    db.commit()
    db.refresh(db_wallet_type)
    return db_wallet_type

@app.get("/wallet_types/", response_model=List[WalletTypeOut])
def list_wallet_types(db: Session = Depends(get_db)):
    return db.query(WalletType).all()

@app.get("/wallet_types/{wallet_type_id}", response_model=WalletTypeOut)
def get_wallet_type(wallet_type_id: int, db: Session = Depends(get_db)):
    wallet_type = db.query(WalletType).filter(WalletType.id == wallet_type_id).first()
    if not wallet_type:
        raise HTTPException(status_code=404, detail="Wallet type not found")
    return wallet_type

@app.delete("/wallet_types/{wallet_type_id}", response_model=WalletTypeOut)
def delete_wallet_type(wallet_type_id: int, db: Session = Depends(get_db)):
    wallet_type = db.query(WalletType).filter(WalletType.id == wallet_type_id).first()
    if not wallet_type:
        raise HTTPException(status_code=404, detail="Wallet type not found")
    db.delete(wallet_type)
    db.commit()
    return wallet_type

# ----- Deposit Addresses Endpoints -----
@app.post("/deposit_addresses/", response_model=DepositAddressOut)
def create_deposit_address(deposit: DepositAddressCreate, db: Session = Depends(get_db)):
    db_deposit = DepositAddress(
        provider_id=deposit.provider_id,
        chain_id=deposit.chain_id,
        wallet_type_id=deposit.wallet_type_id,
        address=deposit.address
    )
    db.add(db_deposit)
    db.commit()
    db.refresh(db_deposit)
    return db_deposit

@app.get("/deposit_addresses/", response_model=List[DepositAddressOut])
def list_deposit_addresses(db: Session = Depends(get_db)):
    return db.query(DepositAddress).all()

@app.get("/deposit_addresses/{deposit_id}", response_model=DepositAddressOut)
def get_deposit_address(deposit_id: int, db: Session = Depends(get_db)):
    deposit = db.query(DepositAddress).filter(DepositAddress.id == deposit_id).first()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit address not found")
    return deposit

@app.delete("/deposit_addresses/{deposit_id}", response_model=DepositAddressOut)
def delete_deposit_address(deposit_id: int, db: Session = Depends(get_db)):
    deposit = db.query(DepositAddress).filter(DepositAddress.id == deposit_id).first()
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit address not found")
    db.delete(deposit)
    db.commit()
    return deposit
