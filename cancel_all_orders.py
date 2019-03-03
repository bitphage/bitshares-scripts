#!/usr/bin/env python

import sys
import json
import logging
import yaml
import click

from bitshares import BitShares
from bitshares.account import Account

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
@click.argument('account')
def main(debug, config, wallet_password, account):
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
    orders = [order['id'] for order in account.openorders if 'id' in order]
    bitshares.cancel(orders, account=account)


if __name__ == '__main__':
    main()
