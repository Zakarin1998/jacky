import requests
import numpy as np
from math import log, sqrt, floor

# Configurazione
everacle_url = "https://api.youroracle.com/prices/historical"
currency_pair = "JCD-USD"
lookback_days = 30
eth_usd = 2600.0  # valore ETH/USD corrente

def fetch_prices(days):
    # Implementa la richiestda all'oracolo
    resp = requests.get(f"{everacle_url}?pair={currency_pair}&days={days}")
    data = resp.json()  # lista di dict {date, price}
    return np.array([d['price'] for d in data])

# Dati storici
daily_prices = fetch_prices(lookback_days)

# Calcolo mediana e deviazione standard
median_price = np.median(daily_prices)
sigma = np.std(daily_prices)
print(f"Mediana JCD/USD: {median_price:.6f}")
print(f"Deviazione σ sul periodo: {sigma:.6f}")

# Definizione range +/- σ e conversione in JCD/ETH
def price_to_jcd_per_eth(price_usd, eth_usd):
    return eth_usd / price_usd

# Range core: median ± σ
grid = [median_price - sigma, median_price + sigma]
jcd_min = price_to_jcd_per_eth(grid[1], eth_usd)
jcd_max = price_to_jcd_per_eth(grid[0], eth_usd)

print(f"Range JCD/ETH core: [{jcd_min:.0f}, {jcd_max:.0f}]")

# Funzione utilitaria per tick Uniswap V3/V4
# tick = floor(log(sqrt(P)) / log(1.0001))
# dove P = price (token1/token0) = ETH per JCD
from math import log

def price_to_tick(price):
    sqrtP = sqrt(price)
    return floor(log(sqrtP) / log(1.0001))

tick_lower = price_to_tick(price_to_jcd_per_eth(median_price + sigma, eth_usd))
tick_upper = price_to_tick(price_to_jcd_per_eth(median_price - sigma, eth_usd))
print(f"TickLower: {tick_lower}, TickUpper: {tick_upper}")