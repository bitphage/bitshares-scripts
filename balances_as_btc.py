#!/usr/bin/env python

import sys
import json
import argparse
import logging
import yaml

from pprint import pprint

from bitshares import BitShares
from bitshares.account import Account
from bitshares.amount import Amount
from bitshares.market import Market

log = logging.getLogger(__name__)


def main():
    def convert_asset(from_value, from_asset, to_asset):
        """ Converts asset to another based on the latest market value

            :param float | from_value: Amount of the input asset
            :param string | from_asset: Symbol of the input asset
            :param string | to_asset: Symbol of the output asset
            :return: float Asset converted to another asset as float value
        """
        market = Market('{}/{}'.format(from_asset, to_asset), bitshares_instance=bitshares)
        ticker = market.ticker()
        latest_price = ticker.get('latest', {}).get('price', None)
        precision = market['base']['precision']

        return round((from_value * latest_price), precision)

    def transform_asset(sum_balances, from_asset, to_asset):
        """ In sum_balances dict, convert one asset into another

            :param dict | sum_balances: dict with balances
            :param str | from_asset: asset to convert from
            :param str | to_asset: destination asset
        """
        if from_asset in sum_balances:
            amount = convert_asset(sum_balances[from_asset], from_asset, to_asset)
            sum_balances[from_asset] = 0
            if to_asset in sum_balances:
                sum_balances[to_asset] += amount
            else:
                sum_balances[to_asset] = amount
        return sum_balances

    parser = argparse.ArgumentParser(
        description='Summarize all assets on all accounts and show BTC equivalent', epilog='Report bugs to: '
    )
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug output'),
    parser.add_argument('-c', '--config', default='./config.yml', help='specify custom path for config file')
    args = parser.parse_args()

    # create logger
    if args.debug == True:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # parse config
    with open(args.config, 'r') as ymlfile:
        conf = yaml.safe_load(ymlfile)

    bitshares = BitShares(node=conf['node_bts'], no_broadcast=True)

    sum_balances = dict()

    for acc in conf['my_accounts']:
        account = Account(acc, bitshares_instance=bitshares)

        # Avail balances
        for i in account.balances:
            asset = i['symbol']
            sum_balances[asset] = sum_balances.setdefault(asset, 0) + i['amount']

        # Balance in orders
        for order in account.openorders:
            asset = order['for_sale']['symbol']
            sum_balances[asset] = sum_balances.setdefault(asset, 0) + order['for_sale']['amount']

        # Margin positions
        for asset, details in account.callpositions.items():
            sum_balances[asset] = sum_balances.setdefault(asset, 0) - details['debt']['amount']

            asset = details['collateral']['asset']['symbol']
            sum_balances[asset] = sum_balances.setdefault(asset, 0) + details['collateral']['amount']

    for asset, amount in sum_balances.items():
        log.debug('Total: {} {}'.format(asset, amount))

    for from_asset, to_asset in conf['transform_assets'].items():
        log.debug('Transforming {} to {}'.format(from_asset, to_asset))
        sum_balances = transform_asset(sum_balances, from_asset, to_asset)

    for asset, amount in sum_balances.items():
        if amount > 0 and asset != conf['btc_asset']:
            log.info('Using direct conversion {:.8f} {} -> {}'.format(amount, asset, conf['btc_asset']))
            sum_balances = transform_asset(sum_balances, asset, conf['btc_asset'])

    print('Accounts value in {}: {:.8f}'.format(conf['btc_asset'], sum_balances[conf['btc_asset']]))


if __name__ == '__main__':
    main()
