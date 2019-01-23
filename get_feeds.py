#!/usr/bin/env python

import sys
import json
import argparse
import logging
import yaml

from pprint import pprint

from bitshares import BitShares
from bitshares.asset import Asset
from bitshares.account import Account

log = logging.getLogger(__name__)

def main():

    parser = argparse.ArgumentParser(
            description='Print current feeds for asset',
            epilog='Report bugs to: ')
    parser.add_argument('-d', '--debug', action='store_true',
            help='enable debug output'),
    parser.add_argument('-c', '--config', default='./config.yml',
            help='specify custom path for config file')
    parser.add_argument('asset')
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
    asset = Asset(args.asset, bitshares_instance=bitshares)
    feeds = asset.feeds

    for feed in feeds:
        print('{}: {}'.format(feed['producer']['name'], feed['settlement_price']))

if __name__ == '__main__':
    main()
