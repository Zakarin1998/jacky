import numpy as np
from math import log, sqrt, floor

def price_to_jcd_per_eth(price_usd, eth_usd):
    return eth_usd / price_usd

def price_to_tick(price):
    sqrtP = sqrt(price)
    return floor(log(sqrtP) / log(1.0001))

def compute_statistics(prices):
    median = np.median(prices)
    sigma = np.std(prices)
    return median, sigma
