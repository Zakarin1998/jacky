import requests
import numpy as np
from dbcores_def.configurations import (
    EVERACLE_URL,
    CURRENCY_PAIR,
    ETH_RESERVE_V1,
    JCD_RESERVE_V1,
    ETH_USD_PRICE,
    POOL_V1_ADDRESS
)

def log_pool_info(logger):
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

def fetch_prices(days):
    resp = requests.get(f"{EVERACLE_URL}?pair={CURRENCY_PAIR}&days={days}")
    resp.raise_for_status()
    data = resp.json()
    return np.array([entry['price'] for entry in data])


def mock_add_liquidity(logger, eth_amount):
    jcd_required = eth_amount * (JCD_RESERVE_V1 / ETH_RESERVE_V1)
    logger.info("\n🟢 Simulazione Add Liquidity on V1:")
    logger.info(f"Depositing {eth_amount:.4f} ETH requires {jcd_required:.2f} JCD")

def mock_trade_jcd_to_eth(logger, jcd_amount):
    k = ETH_RESERVE_V1 * JCD_RESERVE_V1
    new_jcd = JCD_RESERVE_V1 + jcd_amount
    new_eth = k / new_jcd
    eth_out = ETH_RESERVE_V1 - new_eth
    impact = (eth_out / ETH_RESERVE_V1) * 100

    logger.info("\n🔻 Simulazione Trade JCD->ETH on V1:")
    logger.info(f"Selling {jcd_amount:.2f} JCD yields ~{eth_out:.6f} ETH")
    logger.info(f"Price impact: {impact:.2f}%")

def mock_monitor_risk(logger, threshold_eth=0.03):
    logger.info("\n🔍 Monitoraggio V1 ETH Reserve:")
    if ETH_RESERVE_V1 < threshold_eth:
        logger.warning("❗ ETH reserve below threshold, possible dump!")
    else:
        logger.info("✅ Reserve healthy.")
