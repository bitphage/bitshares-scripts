#!/usr/bin/env python

import sys
import json
import argparse
import logging
import yaml

from pprint import pprint

from bitshares import BitShares
from bitshares.asset import Asset

log = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(description='Get asset info', epilog='Report bugs to: ')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug output'),
    parser.add_argument('-c', '--config', default='./config.yml', help='specify custom path for config file')
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
        conf = yaml.safe_load(ymlfile)

    bitshares = BitShares(node=conf['node_bts'], no_broadcast=True)
    asset = Asset(args.asset, full=True, bitshares_instance=bitshares)
    pprint(dict(asset))


if __name__ == '__main__':
    main()
