from uniswap import Uniswap

from constants import (
    VERSION, ADDRESS, PRIVATE_KEY,
    INFURA_KEY
)

from tokens import (
    ETH, DAI, JCD,
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
# Returns the amount of DAI you get for 1 ETH (10^18 wei)
# uniswap.get_price_input(ETH, DAI, 10**18)

# Returns the amount of JCD you get for 0.001 ETH
price_input = uniswap.get_price_input(ETH, JCD, eth_0_001)
print("Amount of JCD you will get for: ", price_input / 10**18)


# Returns the amount of ETH you need to pay (in wei) to get 1000 DAI
x = 1_000
price_output = uniswap.get_price_output(ETH, DAI, x * 10**18)

print(f"ETH needed to get {x} DAI: ", price_output / 10**18)


# Returns the amount of ETH you need to pay to get 20000 JCD
x = 1_000
price_output = uniswap.get_price_output(ETH, JCD, 20 * x * 10**18)

print(f"ETH needed to get {20*x} JCD: ", price_output / 10**18)

