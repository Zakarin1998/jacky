import logging
from decimal import Decimal, getcontext
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import W3, V1_PAIR_ADDRESS, V3_POOL_ADDRESS, SPREAD_THRESHOLD, POLL_INTERVAL

# Simplified ABIs
V1_PAIR_ABI = [{...}]
V3_POOL_ABI = [{...}]

# Increase Decimal precision
getcontext().prec = 28

class PriceMonitor:
    def __init__(self):
        self.logger = logging.getLogger('PriceMonitor')
        logging.basicConfig(level=logging.INFO)
        self.v1 = W3.eth.contract(address=V1_PAIR_ADDRESS, abi=V1_PAIR_ABI)
        self.v3 = W3.eth.contract(address=V3_POOL_ADDRESS, abi=V3_POOL_ABI)
        self.last_status = {}

    def get_v1_price(self):
        reserves = self.v1.functions.getReserves().call()
        r0, r1 = Decimal(reserves[0]), Decimal(reserves[1])
        return None if r0==0 else r1/r0

    def get_v3_price(self):
        slot = self.v3.functions.slot0().call()
        sq = Decimal(slot[0])
        return (sq/(Decimal(2)**96))**2

    def log_prices(self):
        pv1 = self.get_v1_price()
        pv3 = self.get_v3_price()
        if pv1 is None or pv3 is None:
            self.logger.warning('Price fetch failed V1=%s V3=%s', pv1, pv3)
            return
        spread = (pv3-pv1)/pv1*Decimal(100)
        ts = datetime.utcnow().isoformat()+'Z'
        action = 'ALERT' if abs(spread)>Decimal(SPREAD_THRESHOLD) else 'HOLD'
        self.last_status = {'timestamp':ts,'v1':float(pv1),'v3':float(pv3),'spread':float(spread),'action':action}
        self.logger.info(self.last_status)

    def get_last_status(self):
        return self.last_status

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.log_prices,'interval',seconds=POLL_INTERVAL)
        scheduler.start()