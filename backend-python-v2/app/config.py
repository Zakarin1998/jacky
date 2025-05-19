"""General configuration module. """

import os
from dotenv import load_dotenv

load_dotenv()

INFURA_KEY = os.getenv("INFURA_KEY")
RPC_URL = os.getenv("RPC_URL", f"https://mainnet.infura.io/v3/INFURA_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # must be set in environment
CHAIN_ID = int(os.getenv("CHAIN_ID", "1"))  # Ethereum Mainnet
