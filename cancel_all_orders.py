#!/usr/bin/env python

import sys
import json
import logging
import yaml
import click

from bitshares import BitShares
from bitshares.account import Account
from bitshares.market import Market

log = logging.getLogger(__name__)


@click.command()
@click.option('-d', '--debug', default=False, is_flag=True, help='enable debug output')
@click.option(
    '-c', '--config', type=click.File('r'), default='./config.yml', help='specify custom path for config file'
)
@click.option(
    '--wallet-password',
    prompt=True,
    hide_input=True,
    help='master password for bitshares wallet (a prompt will be used if not provided)',
)
@click.option('--buy-only', default=False, is_flag=True, help='cancel only buy orders')
@click.option('--sell-only', default=False, is_flag=True, help='cancel only sell orders')
@click.option('--market', help='cancel orders only on specified market only, format is BASE/QUOTE')
@click.argument('account')
def main(debug, config, wallet_password, buy_only, sell_only, market, account):

    if buy_only and sell_only:
        log.critical('--buy-only and --sell-only are mutually exclusive')
        sys.exit(1)

    # create logger
    if debug == True:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # parse config
    conf = yaml.load(config)

    bitshares = BitShares(node=conf['node_bts'])

    # Wallet unlock
    try:
        bitshares.unlock(wallet_password)
    except WrongMasterPasswordException:
        log.critical('Wrong wallet password provided')
        sys.exit(1)

    account = Account(account, blockchain_instance=bitshares)
    orders = [order for order in account.openorders if 'id' in order]

    if market:
        market = Market(market, blockchain_instance=bitshares)
        market_ids = [market['base']['symbol'], market['quote']['symbol']]
        orders = [
            order
            for order in orders
            if order['base']['symbol'] in market_ids and order['quote']['symbol'] in market_ids
        ]

    if buy_only:
        orders = [order for order in orders if order['base']['symbol'] == market['base']['symbol']]
    elif sell_only:
        orders = [order for order in orders if order['base']['symbol'] == market['quote']['symbol']]

    ids = [order['id'] for order in orders if 'id' in order]

    bitshares.cancel(ids, account=account)


if __name__ == '__main__':
    main()
