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

log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
            description='Show account balances (avail + orders balance)',
            epilog='Report bugs to: ')
    parser.add_argument('-d', '--debug', action='store_true',
            help='enable debug output'),
    parser.add_argument('-c', '--config', default='./config.yml',
            help='specify custom path for config file')
    parser.add_argument('account')
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
        conf = yaml.load(ymlfile)

    bitshares = BitShares(node=conf['node_bts'], no_broadcast=True)

    sum_balances = dict()

    account = Account(args.account, bitshares_instance=bitshares)

    for i in account.balances:
        sum_balances[i['symbol']] = i['amount']

    for order in account.openorders:
        asset = order['for_sale']['symbol']
        sum_balances[asset] = sum_balances.setdefault(asset, 0) + order['for_sale']['amount']

    for key in sum_balances:
        print('{}: {:.8f}'.format(key, sum_balances[key]))

if __name__ == '__main__':
    main()
