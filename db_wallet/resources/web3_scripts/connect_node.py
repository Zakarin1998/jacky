import os
from dotenv import load_dotenv
from web3 import Web3

# Carica le variabili dal file .env
load_dotenv()

# Accesso alle chiavi
infura_key = os.getenv("INFURA_KEY")

# URL del tuo nodo (ad es. Infura/Alchemy)
RPC_URL = f"https://mainnet.infura.io/v3/{infura_key}"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise Exception("Connessione al nodo Ethereum fallita")
print("Connesso alla rete:", web3.eth.chain_id)

