import argparse 
import numpy as np

from dbcores_def.configurations import (
    get_logger,
    LOOKBACK_DAYS,
    ETH_USD_PRICE
)
from dbcores_def.calculation import (
    compute_statistics,
    price_to_jcd_per_eth,
    price_to_tick
)

from dbcores_def.getprice import fetch_prices

from dbcores_def.egmock import (
    log_pool_info,
    mock_add_liquidity,
    mock_trade_jcd_to_eth, 
    mock_monitor_risk
)

def main(args):
    logger = get_logger()

    log_pool_info(logger)

    prices = fetch_prices(LOOKBACK_DAYS)
    median, sigma = compute_statistics(prices)
    logger.info(f"\n📊 Historical Stats ({LOOKBACK_DAYS}d): Median={median:.6f}, σ={sigma:.6f}")

    low = median - sigma
    high = median + sigma
    jcd_min = price_to_jcd_per_eth(high, ETH_USD_PRICE)
    jcd_max = price_to_jcd_per_eth(low, ETH_USD_PRICE)
    tick_lower = price_to_tick(jcd_min)
    tick_upper = price_to_tick(jcd_max)

    logger.info(f"Core LP Range JCD/ETH: [{jcd_min:.0f}, {jcd_max:.0f}]")
    logger.info(f"Ticks: lower={tick_lower}, upper={tick_upper}\n")

    match args.action:
        case 'add_liquidity':
            mock_add_liquidity(logger, args.amount)
        case 'trade':
            mock_trade_jcd_to_eth(logger, args.amount)
        case 'monitor':
            mock_monitor_risk(logger)
        case _:
            logger.info("ℹ️ No action or info selected.")


def test_fetch_prices():
    prices = fetch_prices(7)
    assert isinstance(prices, np.ndarray)
    assert len(prices) > 0
    assert (prices > 0).all()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Unified LP flow script for JCD pools"
    )
    parser.add_argument(
        '--action', 
        type=str,
        default='info',
        choices=['info','add_liquidity','trade','monitor'],
        help='Action to perform'
    )
    parser.add_argument(
        '--amount',
        type=float,
        default=0,
        help='Amount for trade or liquidity'
    )
    
    args = parser.parse_args()
    # main(args)
    test_fetch_prices()