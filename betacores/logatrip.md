# LP Uniswap V4 Automation

Abbiamo creato tre componenti per automatizzare la gestione dei range LP V4 basati su volatilità (σ) e deploy degli hook:

1. 



2. 

**SigmaDynamicFeeHook.sol** con fee dinamiche
---

### 1) Python compute_ticks.py 

calcolo di mediana
calcolo di σ
generazione tick

---

### 2) Solidity: hook dinamico basato su σ

---

### 3) Cron-runner (bash + CLI)

**rebalance_lp.sh** per orchestrare remove/mint/update hook
---


Puoi adattare i parametri (lookback, threshold σ, amount0/amount1) ai tuoi volumi e obiettivi.
