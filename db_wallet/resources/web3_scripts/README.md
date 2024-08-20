Ecco una guida passo-per-passo per costruire un **backend in Python** che interagisce con gli smart contract di Curve Finance per effettuare swap tra due token di una pool. Lo script sarà strutturato in modo modulare, così da poter essere in seguito trasformato in microservizi e integrato in una dashboard minimale con Metamask.

## Sommario

In questo tutorial vedremo:

1. **Prerequisiti**: librerie, chiavi RPC, ABI.
2. **Connessione a un nodo Ethereum** con `web3.py`.
3. **Recupero dell’ABI** del pool Curve.
4. **Funzioni di utilità**: approvazione token, calcolo slippage.
5. **Funzione di swap** vera e propria.
6. **Esempio di script completo** in Python.
7. **Roadmap verso microservizi** e integrazione Metamask.

---

## 1. Prerequisiti

* Python ≥ 3.8
* `web3.py` per l’RPC Ethereum ([web3py.readthedocs.io][1])
* Un provider RPC (Infura/Alchemy) con chiave API
* Gli indirizzi dei token e della pool Curve di interesse
* ABI del pool (scaricabile dal repo ufficiale Curve o da Etherscan) ([GitHub][2])

---

## 2. Connessione a un nodo Ethereum

Installazione:

```bash
pip install web3
```

Configurazione e connessione:

```python
from web3 import Web3

# URL del tuo nodo (ad es. Infura/Alchemy)
RPC_URL = "https://mainnet.infura.io/v3/<YOUR_API_KEY>"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.isConnected():
    raise Exception("Connessione al nodo Ethereum fallita")
print("Connesso alla rete:", web3.eth.chain_id)
```

*Qui usiamo `web3.py`, la libreria Python più diffusa per l’ecosistema Ethereum* ([web3py.readthedocs.io][1]).

---

## 3. Recupero dell’ABI del pool

Ogni pool Curve ha un contratto “Swap” (o “Exchange”) con funzioni come `exchange(i, j, dx, min_dy)` o `exchange_underlying(...)`.

* **Da GitHub**:

  ```bash
  git clone https://github.com/curvefi/curve-contract.git
  ```

  troverai le ABI in `contracts/pools/.../Swap.vy` ([GitHub][2]).
* **Da Etherscan**: cerca l’indirizzo del pool e copia l’ABI dal tab “Contract” ([Ethereum Stack Exchange][3]).

Salva l’ABI in un file locale, per esempio `curve_pool_abi.json`.

---

## 4. Funzioni di utilità

### 4.1 Caricamento del contratto

```python
import json

POOL_ADDRESS = "0x...indirizzo della pool..."
with open("curve_pool_abi.json") as f:
    pool_abi = json.load(f)

pool = web3.eth.contract(address=POOL_ADDRESS, abi=pool_abi)
```

### 4.2 Approve del token

Prima di chiamare `exchange`, bisogna dare allo smart contract il permesso di spendere i tuoi token:

```python
def approve_token(token_address, spender, amount, account):
    with open("erc20_abi.json") as f:
        erc20_abi = json.load(f)
    token = web3.eth.contract(address=token_address, abi=erc20_abi)
    tx = token.functions.approve(spender, amount).buildTransaction({
        "from": account.address,
        "nonce": web3.eth.getTransactionCount(account.address),
    })
    signed = account.signTransaction(tx)
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt
```

*Schema simile a Uniswap e molti DEX*\* ([Ethereum Stack Exchange][4])\* e **CoinsBench** ([CoinsBench][5]).

### 4.3 Calcolo dello slippage

```python
def apply_slippage(amount, slippage_bps=50):
    # slippage_bps: 50 = 0.5%
    return amount * (10_000 - slippage_bps) // 10_000
```

---

## 5. Funzione di swap

```python
from eth_account import Account

def swap_curve(token_i, token_j, dx, slippage_bps, account):
    # 1) Approve
    approve_token(token_i, POOL_ADDRESS, dx, account)
    # 2) Calcola min_dy
    dy = pool.functions.get_dy(token_i_index, token_j_index, dx).call()
    min_dy = apply_slippage(dy, slippage_bps)
    # 3) Costruisci tx di swap
    tx = pool.functions.exchange(token_i_index, token_j_index, dx, min_dy).buildTransaction({
        "from": account.address,
        "nonce": web3.eth.getTransactionCount(account.address),
        "gas": 200_000,
        "gasPrice": web3.eth.gas_price,
    })
    signed = account.signTransaction(tx)
    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
    return web3.eth.waitForTransactionReceipt(tx_hash)
```

* `get_dy` fornisce l’output teorico prima delle fee ([docs.curve.fi][6]).
* `exchange` esegue lo swap vero e proprio.

---

## 6. Script Python completo

```python
import json
from web3 import Web3
from eth_account import Account

# --- Configurazione ---
RPC_URL = "https://mainnet.infura.io/v3/<YOUR_API_KEY>"
web3 = Web3(Web3.HTTPProvider(RPC_URL))
PRIVATE_KEY = "<TUO_PRIVATE_KEY>"
account = Account.from_key(PRIVATE_KEY)

with open("curve_pool_abi.json") as f: pool_abi = json.load(f)
with open("erc20_abi.json")   as f: erc20_abi = json.load(f)

POOL_ADDRESS = "0x...pool..."
pool = web3.eth.contract(address=POOL_ADDRESS, abi=pool_abi)

# Mappa token→index nella pool
token_index = {
    "USDC": 1,
    "DAI": 0,
    # aggiungi altri token qui
}

def approve_token(token_addr, spender, amount):
    token = web3.eth.contract(address=token_addr, abi=erc20_abi)
    tx = token.functions.approve(spender, amount).buildTransaction({
        "from": account.address,
        "nonce": web3.eth.getTransactionCount(account.address),
    })
    signed = account.signTransaction(tx)
    return web3.eth.waitForTransactionReceipt(
        web3.eth.sendRawTransaction(signed.rawTransaction)
    )

def apply_slippage(amount, bps=50):
    return amount * (10_000 - bps) // 10_000

def swap(token_in, token_out, amount_in, slippage_bps=50):
    i = token_index[token_in]
    j = token_index[token_out]
    # approve
    approve_token(token_addresses[token_in], POOL_ADDRESS, amount_in)
    # calcola get_dy
    dy = pool.functions.get_dy(i, j, amount_in).call()
    min_dy = apply_slippage(dy, slippage_bps)
    # swap
    tx = pool.functions.exchange(i, j, amount_in, min_dy).buildTransaction({
        "from": account.address,
        "nonce": web3.eth.getTransactionCount(account.address),
        "gas": 200_000,
        "gasPrice": web3.eth.gas_price,
    })
    signed = account.signTransaction(tx)
    receipt = web3.eth.waitForTransactionReceipt(
        web3.eth.sendRawTransaction(signed.rawTransaction)
    )
    print("Swap completato:", receipt.transactionHash.hex())
    return receipt

if __name__ == "__main__":
    # Esempio: swap 100 USDC→DAI (6 decimali)
    amount = 100 * 10**6
    swap("USDC", "DAI", amount, slippage_bps=30)
```

---

## 7. Prossimi passi: da script a microservizi

1. **Separazione dei componenti** (approval, quote, execution) in API distinte (FastAPI/Flask).
2. **Database** per storicizzare swap e parametri.
3. **Job scheduler** per swap ricorrenti o bot di arbitraggio ([jondidathing.hashnode.dev][7]).
4. **Web frontend minimale** (React + Web3.js) per mettere in pausa/avviare swap via Metamask.

Questa architettura modulare sarà la base per costruire la tua **dashboard customizzata** e i futuri automatismi di trading. Buon coding! ❤️

[1]: https://web3py.readthedocs.io/en/stable/resources.html?utm_source=chatgpt.com "Resources and Learning Material — web3.py 7.11.0 documentation"
[2]: https://github.com/curvefi/curve-contract?utm_source=chatgpt.com "Vyper contracts used in Curve.fi exchange pools. - GitHub"
[3]: https://ethereum.stackexchange.com/questions/102936/where-can-i-find-the-polygon-curve-fi-interfaces-for-solidity?utm_source=chatgpt.com "Where can I find the polygon.curve.fi interfaces for solidity?"
[4]: https://ethereum.stackexchange.com/questions/161829/how-to-swap-one-coin-to-another-in-web3-py-using-uniswap-contracts?utm_source=chatgpt.com "How to swap one coin to another in Web3.py using Uniswap ..."
[5]: https://coinsbench.com/interact-with-cronos-single-usdc-lp-with-web3-py-1e14c62a0d9c?utm_source=chatgpt.com "web3.py — Interact with CRONOS SINGLE/USDC LP - CoinsBench"
[6]: https://docs.curve.fi/integration/rate-provider/?utm_source=chatgpt.com "Rate Provider - Curve Technical Docs"
[7]: https://jondidathing.hashnode.dev/black-swan-arbitrage?utm_source=chatgpt.com "Making Money Through Crypto Arbitrage Using Python"
