#!/usr/bin/env python

import json
import logging
import string
import sys
from pprint import pprint

import click
import yaml
from bitshares import BitShares
from bitshares.account import Account
from bitshares.exceptions import MissingKeyError
from bitsharesbase import operations
from bitsharesbase.account import PasswordKey, PublicKey
from graphenestorage.exceptions import WrongMasterPasswordException

from bitsharesscripts.functions import generate_password

log = logging.getLogger(__name__)

key_types = ['active', 'owner', 'memo']


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
@click.option('-p', '--password', help='manually specify a password (if not, a random will be generated)')
@click.option('--broadcast', default=False, is_flag=True, help='broadcast transaction')
@click.argument('parent_account')
@click.argument('account_name')
def main(debug, config, wallet_password, password, broadcast, parent_account, account_name):
    """ Use this script to create new account. By default, a random password will be
        generated. By default, transaction will not be broadcasted (dry-run mode).
    """
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
    conf = yaml.safe_load(config)

    b = not broadcast
    bitshares = BitShares(node=conf['node_bts'], nobroadcast=b)
    account = Account(parent_account, bitshares_instance=bitshares)

    # Wallet unlock
    try:
        bitshares.unlock(wallet_password)
    except WrongMasterPasswordException:
        log.critical('Wrong wallet password provided')
        sys.exit(1)

    # random password
    if password:
        password = password
    else:
        password = generate_password()

    print('password: {}\n'.format(password))

    key = dict()
    for key_type in key_types:
        # PasswordKey object
        k = PasswordKey(account_name, password, role=key_type)

        privkey = k.get_private_key()
        print('{} private: {}'.format(key_type, str(privkey)))  # we need explicit str() conversion!

        # pubkey with default prefix GPH
        pubkey = k.get_public_key()

        # pubkey with correct prefix
        key[key_type] = format(pubkey, bitshares.prefix)
        print('{} public: {}\n'.format(key_type, key[key_type]))

    try:
        bitshares.create_account(
            account_name,
            registrar=parent_account,
            referrer=account['id'],
            referrer_percent=0,
            password=password,
            storekeys=broadcast,
        )
    except MissingKeyError:
        log.critical('No key for {} in storage, use `uptick addkey` to add'.format(parent_account))
        sys.exit(1)


if __name__ == '__main__':
    main()
