# In dbcores_def/egmock.py
import requests
import numpy as np
from dbcores_def.configurations import CURRENCY_PAIR

def fetch_prices(days):
    # Separiamo simboli per coin ID e valuta vs (USD)
    coin_id, vs = CURRENCY_PAIR.lower().split("-")  # es: "jcd-usd" → "jcd", "usd"
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs,
        "days": days
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    prices = data.get("prices", [])
    # Estraiamo solo il valore di prezzo da ogni coppia [timestamp, price]
    return np.array([p[1] for p in prices])
