import logging
import requests
import numpy as np
from math import log, sqrt, floor
import argparse

# === CONFIGURATION ===
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

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LPFlow")

# === PRICE DATA FUNCTIONS ===
def fetch_prices(days):
    """
    Fetch historical daily prices for JCD-USD over given lookback days.
    Returns a numpy array of floats.
    """
    resp = requests.get(f"{EVERACLE_URL}?pair={CURRENCY_PAIR}&days={days}")
    resp.raise_for_status()
    data = resp.json()  # expect list of {'date':..., 'price':...}
    return np.array([entry['price'] for entry in data])

# === STATISTICAL CALCULATIONS ===
def compute_statistics(prices):
    median_price = np.median(prices)
    sigma = np.std(prices)
    return median_price, sigma

# === UNISWAP TICK CALCULATIONS ===
def price_to_jcd_per_eth(price_usd, eth_usd):
    return eth_usd / price_usd

def price_to_tick(price):
    """
    Convert price P (token1/token0 = ETH per JCD) to Uniswap V3/V4 tick index.
    tick = floor(log(sqrt(P)) / log(1.0001))
    """
    sqrtP = sqrt(price)
    return floor(log(sqrtP) / log(1.0001))

# === LOGGING AND SIMULATION ===
def log_pool_info():
    jcd_per_eth = JCD_RESERVE_V1 / ETH_RESERVE_V1
    eth_per_jcd = ETH_RESERVE_V1 / JCD_RESERVE_V1
    jcd_usd_price = ETH_USD_PRICE * eth_per_jcd

    logger.info("🔹 Uniswap V1 Pool Info:")
    logger.info(f"Pool Address: {POOL_V1_ADDRESS}")
    logger.info(f"ETH Reserve: {ETH_RESERVE_V1:.6f} ETH")
    logger.info(f"JCD Reserve: {JCD_RESERVE_V1:.2f} JCD")
    logger.info(f"1 ETH = {jcd_per_eth:.2f} JCD")
    logger.info(f"1 JCD = {eth_per_jcd:.8f} ETH")
    logger.info(f"JCD Price (USD): ${jcd_usd_price:.6f}")


def simulate_add_liquidity(eth_amount):
    jcd_required = eth_amount * (JCD_RESERVE_V1 / ETH_RESERVE_V1)
    logger.info("\n🟢 Simulazione Add Liquidity on V1:")
    logger.info(f"Depositing {eth_amount:.4f} ETH requires {jcd_required:.2f} JCD")


def simulate_trade_jcd_to_eth(jcd_amount):
    k = ETH_RESERVE_V1 * JCD_RESERVE_V1
    new_jcd = JCD_RESERVE_V1 + jcd_amount
    new_eth = k / new_jcd
    eth_out = ETH_RESERVE_V1 - new_eth
    impact = (eth_out / ETH_RESERVE_V1) * 100
    logger.info("\n🔻 Simulazione Trade JCD->ETH on V1:")
    logger.info(f"Selling {jcd_amount:.2f} JCD yields ~{eth_out:.6f} ETH")
    logger.info(f"Price impact: {impact:.2f}%")


def monitor_risk(threshold_eth=0.03):
    logger.info("\n🔍 Monitoraggio V1 ETH Reserve:")
    if ETH_RESERVE_V1 < threshold_eth:
        logger.warning("❗ ETH reserve below threshold, possible dump!")
    else:
        logger.info("✅ Reserve healthy.")

# === MAIN FLOW ===
def main(args):
    # 1. Log V1 pool info
    log_pool_info()

    # 2. Fetch and compute statistics
    prices = fetch_prices(LOOKBACK_DAYS)
    median_price, sigma = compute_statistics(prices)
    logger.info(f"\n📊 Historical Stats ({LOOKBACK_DAYS}d): Median={median_price:.6f}, σ={sigma:.6f}")

    # 3. Compute core LP range based on median ± σ
    low = median_price - sigma
    high = median_price + sigma
    jcd_min = price_to_jcd_per_eth(high, ETH_USD_PRICE)
    jcd_max = price_to_jcd_per_eth(low, ETH_USD_PRICE)
    tick_lower = price_to_tick(price_to_jcd_per_eth(high, ETH_USD_PRICE))
    tick_upper = price_to_tick(price_to_jcd_per_eth(low, ETH_USD_PRICE))
    logger.info(f"Core LP Range JCD/ETH: [{jcd_min:.0f}, {jcd_max:.0f}]")
    logger.info(f"Ticks: lower={tick_lower}, upper={tick_upper}\n")

    # 4. Execute chosen action
    if args.action == 'add_liquidity':
        simulate_add_liquidity(args.amount)
    elif args.action == 'trade':
        simulate_trade_jcd_to_eth(args.amount)
    elif args.action == 'monitor':
        monitor_risk()
    else:
        logger.info("ℹ️ No action or info selected.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Unified LP flow script for JCD pools")
    parser.add_argument('--action', type=str, default='info', choices=['info','add_liquidity','trade','monitor'],
                        help='Action to perform')
    parser.add_argument('--amount', type=float, default=0,
                        help='Amount for trade or liquidity')
    args = parser.parse_args()
    main(args)
