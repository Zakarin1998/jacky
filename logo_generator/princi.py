# jcd_price_monitor.py
# Monitor prices of JChanDollar (JCD) on Uniswap V1 and V3
# Requires: Python 3.8+, web3.py, python-dotenv, apscheduler, decimal, pandas

import os
import time
import logging
from decimal import Decimal, getcontext
from datetime import datetime
from web3 import Web3
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

# Increase precision for Decimal
getcontext().prec = 28

# Load environment variables
load_dotenv()
RPC_URL = os.getenv('RPC_URL')  # e.g. https://mainnet.infura.io/v3/YOUR_KEY
PRIVATE_KEY = os.getenv('PRIVATE_KEY')  # optional, if needed

# Uniswap V1 & V3 contract addresses
JCD_ADDRESS = Web3.to_checksum_address(os.getenv('JCD_ADDRESS'))  # JCD token
WETH_ADDRESS = Web3.to_checksum_address(os.getenv('WETH_ADDRESS'))  # WETH token
V1_FACTORY = Web3.to_checksum_address(os.getenv('V1_FACTORY'))
V3_POOL = Web3.to_checksum_address(os.getenv('V3_POOL'))  # specific JCD/WETH V3 pool

# ABIs (simplified interfaces)
V1_PAIR_ABI = [
    {"constant": True, "inputs": [], "name": "getReserves", "outputs": [
        {"name": "_reserve0", "type": "uint112"},
        {"name": "_reserve1", "type": "uint112"},
        {"name": "_blockTimestampLast", "type": "uint32"}
    ], "type": "function"},
]
V3_POOL_ABI = [
    {"inputs": [], "name": "slot0", "outputs": [
        {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
        {"internalType": "int24", "name": "tick", "type": "int24"},
        {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
        {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
        {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
        {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
        {"internalType": "bool", "name": "unlocked", "type": "bool"}
    ], "stateMutability": "view", "type": "function"}
]

# Initialize web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
V1_PAIR = w3.eth.contract(address=None, abi=V1_PAIR_ABI)  # placeholder
V3_CONTRACT = w3.eth.contract(address=V3_POOL, abi=V3_POOL_ABI)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler('jcd_monitor.log'), logging.StreamHandler()]
)


def get_v1_price():
    # Derive pair address via factory (optional): here assume direct pair address in env
    pair_address = Web3.to_checksum_address(os.getenv('V1_PAIR'))
    pair = w3.eth.contract(address=pair_address, abi=V1_PAIR_ABI)
    reserves = pair.functions.getReserves().call()
    # reserve0 = JCD, reserve1 = WETH
    r0 = Decimal(reserves[0])
    r1 = Decimal(reserves[1])
    if r0 == 0:
        return None
    return r1 / r0  # ETH per JCD


def get_v3_price():
    slot0 = V3_CONTRACT.functions.slot0().call()
    sqrt_price_x96 = Decimal(slot0[0])
    # price = (sqrtPriceX96 / 2**96)**2
    price = (sqrt_price_x96 / (Decimal(2) ** 96)) ** 2
    return price  # ETH per JCD


def log_prices():
    price_v1 = get_v1_price()
    price_v3 = get_v3_price()
    if not price_v1 or not price_v3:
        logging.warning('One of the prices is None: V1=%s V3=%s', price_v1, price_v3)
        return

    spread = (price_v3 - price_v1) / price_v1 * Decimal(100)
    ts = datetime.utcnow().isoformat() + 'Z'
    action = 'HOLD'
    if abs(spread) > Decimal(os.getenv('SPREAD_THRESHOLD', '3')):
        action = 'ALERT'
    logging.info(f"[{ts}] V1: {price_v1:.8f} ETH | V3: {price_v3:.8f} ETH | Spread: {spread:.2f}% | ACTION: {action}")


def main():
    interval = int(os.getenv('POLL_INTERVAL', '15'))  # seconds
    scheduler = BlockingScheduler()
    scheduler.add_job(log_prices, 'interval', seconds=interval)
    logging.info('Starting JCD price monitor...')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info('Scheduler stopped.')


if __name__ == '__main__':
    main()

# .env example:
# RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_KEY
# V1_PAIR=0xYourUniswapV1PairAddress
# V3_POOL=0xYourUniswapV3PoolAddress
# JCD_ADDRESS=0xYourJCDAddress
# WETH_ADDRESS=0xC02aaa39b223FE8D0A0E5C4F27eAD9083C756Cc2
# SPREAD_THRESHOLD=3
# POLL_INTERVAL=15
