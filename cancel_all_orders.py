#!/usr/bin/env python

import sys
import json
import argparse
import logging
import yaml

from bitshares import BitShares
from bitshares.account import Account

log = logging.getLogger(__name__)

def main():

    parser = argparse.ArgumentParser(
            description='Cancel all orders on account',
            epilog='Report bugs to: ')
    parser.add_argument('-d', '--debug', action='store_true',
            help='enable debug output'),
    parser.add_argument('-c', '--config', default='./common.yml',
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

    bitshares = BitShares(node=conf['node_bts'])
    a = Account(args.account, blockchain_instance=bitshares)
    orders = [order['id'] for order in a.openorders if 'id' in order]
    bitshares.cancel(orders, account=a)

if __name__ == '__main__':
    main()
