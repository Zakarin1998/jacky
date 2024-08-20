from web3 import Web3
from app.config import get_settings

class EthereumClient:
    def __init__(self):
        cfg = get_settings()
        url = f"https://mainnet.infura.io/v3/{cfg.infura_key}"
        self.web3 = Web3(Web3.HTTPProvider(url))

        if not self.web3.is_connected():
            raise ConnectionError("Fallita connessione a Ethereum")

    @property
    def chain_id(self) -> int:
        return self.web3.eth.chain_id

    def deploy_contract(self, abi: dict, bytecode: str, constructor_args: tuple = ()):  
        """Esegue il deploy e ritorna l'indirizzo."""
        cfg = get_settings()
        acct = self.web3.eth.account.from_key(cfg.private_key)
        contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)

        tx = contract.constructor(*constructor_args).build_transaction({
            "chainId": self.chain_id,
            "gas": 5_000_000,
            "gasPrice": self.web3.to_wei("50", "gwei"),
            "nonce": self.web3.eth.get_transaction_count(acct.address),
        })
        signed = acct.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.contractAddress