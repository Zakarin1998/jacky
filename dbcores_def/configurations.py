# === CONFIGURATION ===
import logging

def get_logger(name="LPFlow"):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)

# Historical price oracle
EVERACLE_URL = "https://api.youroracle.com/prices/historical"
CURRENCY_PAIR = "JCD-USD"
LOOKBACK_DAYS = 30
ETH_USD_PRICE = 2600.0  # update to current

# Uniswap V1 Pool constants
ETH_RESERVE_V1 = 0.066931431537039094
JCD_RESERVE_V1 = 12060.717
POOL_V1_ADDRESS = "0x657184E418D43A661a91d567182Dc3D1A4179ec4"

# Uniswap V4 LP parameters (placeholder values)
LP_V4_ADDRESS = "0xYourV4PoolAddress"
LP_FEE_TIER = 30  # 0.3%
