from web3 import Web3
from web3.exceptions import TransactionNotFound
from app.config import RPC_URL, PRIVATE_KEY, CHAIN_ID
from app.logging_conf import logger

class EthereumClient:
    """Ethereum web3 wrapper class."""

    def __init__(self, rpc_url: str, private_key: str, chain_id: int):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            logger.error("Web3 provider not connected: %s", rpc_url)
            raise ConnectionError("Unable to connect to Ethereum provider")
        logger.info("Connected to Ethereum provider %s", rpc_url)

        self.account = self.w3.eth.account.from_key(private_key)
        self.chain_id = chain_id
        logger.info("Using account %s on chain %d", self.account.address, self.chain_id)

    def get_contract(self, address: str, abi: list):
        checksum = self.w3.to_checksum_address(address)
        logger.debug("Loading contract at %s", checksum)
        return self.w3.eth.contract(address=checksum, abi=abi)

    def health(self) -> bool:
        """Checks basic provider and network reachability."""

        try:
            block = self.w3.eth.block_number
            logger.info("Current block number: %d", block)
            return { "status": "ok", "block_number": block }
        except Exception as e:
            logger.error("Health check failed: %s", e)
            return { "status": "ko", "block_number": 0 }

    def transfer_eth(self, to_address: str, amount_wei: int, gas_price_wei: int = None) -> str:
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        tx = {
            "to": self.w3.to_checksum_address(to_address),
            "value": amount_wei,
            "gas": 21000,
            "nonce": nonce,
            "chainId": self.chain_id,
        }
        if gas_price_wei is not None:
            tx["gasPrice"] = gas_price_wei
        else:
            tx["maxFeePerGas"] = self.w3.eth.gas_price
            tx["maxPriorityFeePerGas"] = self.w3.to_wei(2, 'gwei')

        signed = self.w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        logger.info("Sent ETH transfer: %s", tx_hash.hex())
        return tx_hash.hex()