#!/usr/bin/env python

import json
import logging
import random
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

log = logging.getLogger(__name__)

key_types = ['active', 'owner', 'memo']


def generate_password(size=53, chars=string.ascii_letters + string.digits):
    """ Generate random word with letters and digits
    """
    return ''.join(random.choice(chars) for x in range(size))


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
@click.argument('account_name')
def main(debug, config, wallet_password, password, broadcast, account_name):
    """ Use this script to change account keys. By default, a random will be
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
    account = Account(account_name, bitshares_instance=bitshares)

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

    # prepare for json format
    account['options']['memo_key'] = key['memo']
    owner_key_authority = [[key['owner'], 1]]
    active_key_authority = [[key['active'], 1]]
    owner_accounts_authority = []
    active_accounts_authority = []
    posting_accounts_authority = []

    s = {
        'account': account['id'],
        'new_options': account['options'],
        'owner': {'account_auths': owner_accounts_authority, 'key_auths': owner_key_authority, 'weight_threshold': 1},
        'active': {
            'account_auths': active_accounts_authority,
            'key_auths': active_key_authority,
            'weight_threshold': 1,
        },
        'fee': {'amount': 0, 'asset_id': '1.3.0'},
        'extensions': {},
        'prefix': bitshares.prefix,
    }

    # pprint(s)
    op = operations.Account_update(**s)

    try:
        bitshares.finalizeOp(op, account_name, 'owner')
    except MissingKeyError:
        log.critical('No key for {} in storage, use `uptick addkey` to add'.format(account_name))
        sys.exit(1)


if __name__ == '__main__':
    main()
