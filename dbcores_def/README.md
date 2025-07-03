## 📘 README.md – JCD LPFlow Simulation

Demonstration of proper separation of concerns (config, logic, simulation, I/O), and the code is quite clean.

Now we lay out next steps with clarity, including the real oracle integration task.

---

Per ottenere una **modularità massima** e migliorare la **leggibilità e manutenibilità**, possiamo dividere il codice in più moduli, seguendo una struttura chiara e scalabile. Di seguito una proposta strutturata in moduli:

---

### Overview

This project simulates a **Uniswap V1-style liquidity pool** for the fictional `JCD/ETH` trading pair. It provides tooling to:

* Inspect pool reserves and pricing.
* Simulate liquidity provision.
* Simulate trades (JCD → ETH).
* Monitor risk based on ETH reserve levels.

It also integrates with a mock price oracle to derive historical statistics (median, standard deviation), useful for planning LP strategies.

---

### 🔧 Features

* 🧠 **Price Analysis**: Pulls historical JCD/USD prices from an external oracle to compute a statistical range.
* 🧪 **Simulations**:

  * Liquidity provision based on current pool ratio.
  * Trade simulations with price impact estimation.
  * Risk monitor for ETH depletion alert.
* 🗂️ Clean structure with modular configuration and calculations.

---

### ✅ Vantaggi della modularizzazione

* **Manutenibilità**: modifiche isolate senza effetto collaterale.
* **Testabilità**: ogni modulo può essere testato singolarmente.
* **Estendibilità**: più facile aggiungere supporto per Uniswap V3/V4 in moduli separati.

---

### 🖥️ Usage

```bash
python __main__.py --action [info|add_liquidity|trade|monitor] --amount <value>
```

#### Example Commands:

```bash
# Just show pool stats + core range
python __main__.py --action info

# Simulate adding 0.02 ETH worth of liquidity
python __main__.py --action add_liquidity --amount 0.02

# Simulate selling 100 JCD to ETH
python __main__.py --action trade --amount 100

# Monitor ETH reserve health
python __main__.py --action monitor
```

---


## 📁 Struttura dei file:

```
jacky/
│
├── __main__.py                     # Entry point principale
├── dbcores_def/
│   ├── calculation.py              # Calcoli statistici (mediana, dev standard)
│   ├── configurations.py           # Config statiche, log
│   ├── egmock.py                   # 
│   ├── __main__.py
│   └── egmock.py                   # Mock trade, add lp,monitor riserve. fprice
│                                   # Conversioni di prezzo in tick Uniswap
│
└── resources/
    └── data.csv                    # Risorse di dati
```


---

### ⚠️ Current Limitation

The script currently fails when attempting to fetch historical price data from a **placeholder oracle endpoint**:

```txt
https://api.youroracle.com/prices/historical?pair=JCD-USD&days=30
```

This results in a `NameResolutionError` since the domain is not live.

---

## ✅ Next Steps

### 🔗 Replace the Fake Oracle

> 🔨 **Task**: Integrate a working JCD/USD oracle or mock with real data locally.

1. **Option 1 – Local JSON File as Oracle Mock**
   Replace `fetch_prices()` with a loader for a local historical data file:

   ```python
   def fetch_prices(days):
       with open('mock_data/jcd_usd_prices.json') as f:
           return np.array(json.load(f))
   ```

2. **Option 2 – Use Public API (e.g., Coingecko, CryptoCompare)**
   If JCD were real:

   ```python
   EVERACLE_URL = "https://api.coingecko.com/api/v3/coins/jcd/market_chart"
   ```

3. **Enhance Error Handling** in `fetch_prices()`:

   ```python
   try:
       resp = requests.get(...)
       resp.raise_for_status()
   except requests.exceptions.RequestException as e:
       logger.error(f"Failed to fetch oracle data: {e}")
       return np.array([])
   ```

---

### 🔮 Future Features

* [ ] Replace fake oracle with live or local data.
* [ ] Implement Uniswap V2/V3/V4 style swap simulations.
* [ ] Visualize tick range on a chart.
* [ ] Add CSV/JSON output for stats and simulations.
* [ ] Accept price override via CLI args for easier testing.
* [ ] Real liquidity accounting, LP share calc, fees, impermanent loss sim.

---

### 🧑‍💻 Requirements

* Python 3.9+
* Packages:

  ```bash
  pip install requests numpy
  ```

---

### ✍️ Author Notes

This is an MVP for LP flow simulations and core range planning. It's modular, testable, and ideal for future expansion (real oracles, GUI, integrations with chain data, etc.).

---

Let me know if you'd like:

* A sample `jcd_usd_prices.json` file
* Enhanced CLI interface (e.g., add `--oracle-source`)
* Docker setup for portability

Ready for the next phase. 🚀
