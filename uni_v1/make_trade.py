from uniswap import Uniswap
from constants import (
    VERSION, ADDRESS, PRIVATE_KEY, INFURA_KEY
)
from tokens import (
    ETH, SCHAP, JCD
)

# Some ETH subunits we will use
eth_1_0 = 10**18 # $3500
eth_0_1 = 10**17 # $350
eth_0_01 = 10**16 # $35
eth_0_001 = 10**15 # $3.5
eth_0_0001 = 10**14 # $0.35
eth_0_00001 = 10**13

# Uniswap Client Instance
url = f'https://mainnet.infura.io/v3/{INFURA_KEY}'

uniswap=Uniswap(
    address=ADDRESS,
    private_key=PRIVATE_KEY,
    version=VERSION,
    provider=url
)

# Sell around 0.013 ETH for JCD
eth_qty = eth_0_01 + (3*eth_0_001)

uniswap.make_trade(ETH,SCHAP,eth_qty)
