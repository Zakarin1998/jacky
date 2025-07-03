import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UniswapV1_JCD_Info")

# === Constants ===
ETH_RESERVE = 0.066931431537039094
JCD_RESERVE = 12060.717

SYMBOL = "JCD"
NAME = "JChanDollar"
ERC20_ADDRESS = "0x0Ed024d39d55e486573EE32e583bC37Eb5A6271f"
POOL_V1_ADDRESS = "0x657184E418D43A661a91d567182Dc3D1A4179ec4"

WEBSITE = "https://jchandollar.vip"
TWITTER = "@JChanDollar"

# Example ETH price in USD
ETH_USD_PRICE = 3435.70  # update this with current price if needed

# === Calculations ===
jcd_per_eth = JCD_RESERVE / ETH_RESERVE
eth_per_jcd = ETH_RESERVE / JCD_RESERVE
jcd_usd_price = ETH_USD_PRICE * eth_per_jcd

# === Logging Information ===
logger.info("🔹 Token Info:")
logger.info(f"Symbol: {SYMBOL}")
logger.info(f"Name: {NAME}")
logger.info(f"ERC20 Address: {ERC20_ADDRESS}")
logger.info(f"Website: {WEBSITE}")
logger.info(f"Twitter: {TWITTER}")

logger.info("\n🔹 Uniswap V1 Pool Info:")
logger.info(f"Pool V1 Address: {POOL_V1_ADDRESS}")
logger.info(f"ETH Reserve: {ETH_RESERVE} ETH")
logger.info(f"JCD Reserve: {JCD_RESERVE} {SYMBOL}")

logger.info("\n🔹 Derived Prices and Ratios:")
logger.info(f"Current Rate: {jcd_per_eth:.2f} JCD / 1 ETH")
logger.info(f"Current Rate: {eth_per_jcd:.8f} ETH / 1 JCD")
logger.info(f"ETH Price (USD): ${ETH_USD_PRICE:.2f}")
logger.info(f"{SYMBOL} Price (USD): ${jcd_usd_price:.6f}")

# === Additional Notes ===
logger.info("\n🔹 Additional Notes:")
logger.info("This data is based on Uniswap V1, which may have limited liquidity and should be cross-verified.")
