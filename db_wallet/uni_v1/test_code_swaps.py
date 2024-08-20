from uniswap import Uniswap

from constants import (
    ADDRESS, PRIVATE_KEY, INFURA_KEY
)

from tokens import (
    ETH, WETH, ALCX
)
url = f'https://mainnet.infura.io/v3/{INFURA_KEY}'
# Note : this script use both Uniswap version 2 and 3. 
uniswap2 = Uniswap(
    address=ADDRESS, private_key=PRIVATE_KEY, version=2, provider=url
)

uniswap=Uniswap(
    address=ADDRESS, private_key=PRIVATE_KEY, version=3, provider=url
)

# First print
impact = uniswap.estimate_price_impact(
    WETH, ALCX,
    1 * 10 ** 18, 500
)
print("1 ETH to ALCX @ V3 (0.05pct fee pool): " + str(impact))

# Second print
impact = uniswap.estimate_price_impact(
    WETH, ALCX,
    1 * 10 ** 18, 3000
)
print("1 ETH to ALCX @ V3 (0.3pct fee pool): " + str(impact))

# Third print
impact = uniswap.estimate_price_impact(
    WETH, ALCX,
    1 * 10 ** 18, 10000
)
print("1 ETH to ALCX @ V3 (1pct fee pool): " + str(impact))

impact = uniswap2.estimate_price_impact(
    WETH, ALCX, 1 * 10 ** 18
)
print("1 ETH to ALCX @ V2: " + str(impact))
