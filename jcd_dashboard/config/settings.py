import os
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
deploy_env = os.getenv('env', 'production')
load_dotenv(dotenv_path='.env' if deploy_env=='development' else None)

# RPC client
RPC_URL = os.getenv('RPC_URL')
W3 = Web3(Web3.HTTPProvider(RPC_URL))

# Uniswap addresses
V1_PAIR_ADDRESS = Web3.to_checksum_address(os.getenv('V1_PAIR_ADDRESS'))
V3_POOL_ADDRESS = Web3.to_checksum_address(os.getenv('V3_POOL_ADDRESS'))
JCD_ADDRESS = Web3.to_checksum_address(os.getenv('JCD_ADDRESS'))
WETH_ADDRESS = Web3.to_checksum_address(os.getenv('WETH_ADDRESS'))

# Monitoring parameters
SPREAD_THRESHOLD = float(os.getenv('SPREAD_THRESHOLD', '3'))
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', '15'))

# Flask server config
FLASK_ENV = deploy_env
PORT = int(os.getenv('PORT', '5000'))