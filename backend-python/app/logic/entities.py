from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    infura_key: str
    private_key: str  
    account_address: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class DeployRequest(BaseModel):
    name: str
    symbol: str
    total_supply: int