#!/usr/bin/env python

import sys
from pprint import pformat

import click
from bitshares.account import Account
from bitshares.exceptions import MissingKeyError
from bitsharesbase import operations
from bitsharesbase.account import PasswordKey
from uptick.decorators import unlock

from bitsharesscripts.decorators import chain, common_options
from bitsharesscripts.functions import generate_password

key_types = ['active', 'owner', 'memo']


@click.command()
@common_options
@chain
@unlock
@click.option('-p', '--password', help='manually specify a password (if not, a random will be generated)')
@click.option('--broadcast', default=False, is_flag=True, help='broadcast transaction')
@click.argument('account_name')
@click.pass_context
def main(ctx, password, broadcast, account_name):
    """ Use this script to change account keys. By default, a random will be
        generated. By default, transaction will not be broadcasted (dry-run mode).
    """
    account = Account(account_name, bitshares_instance=ctx.bitshares)

    # random password
    if not password:
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
        key[key_type] = format(pubkey, ctx.bitshares.prefix)
        print('{} public: {}\n'.format(key_type, key[key_type]))

    # prepare for json format
    account['options']['memo_key'] = key['memo']
    owner_key_authority = [[key['owner'], 1]]
    active_key_authority = [[key['active'], 1]]
    owner_accounts_authority = []
    active_accounts_authority = []

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
        'prefix': ctx.bitshares.prefix,
    }

    ctx.log.debug(pformat(s))
    op = operations.Account_update(**s)

    if not broadcast:
        ctx.log.info('Not broadcasting!')
        sys.exit(0)

    try:
        ctx.bitshares.finalizeOp(op, account_name, 'owner')
    except MissingKeyError:
        ctx.log.critical('No key for {} in storage, use `uptick addkey` to add'.format(account_name))
        sys.exit(1)


if __name__ == '__main__':
    main()
