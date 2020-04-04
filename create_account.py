#!/usr/bin/env python

import sys

import click
from bitshares.account import Account
from bitshares.exceptions import MissingKeyError
from uptick.decorators import unlock

from bitsharesscripts.decorators import chain, common_options
from bitsharesscripts.functions import generate_password, get_keys_from_password


@click.command()
@common_options
@chain
@unlock
@click.option('-p', '--password', help='manually specify a password (if not, a random will be generated)')
@click.option('--broadcast', default=False, is_flag=True, help='broadcast transaction')
@click.argument('parent_account')
@click.argument('account_name')
@click.pass_context
def main(ctx, password, broadcast, parent_account, account_name):
    """Use this script to create new account.

    By default, a random password will be generated. By default, transaction will not be broadcasted (dry-run mode).
    """
    account = Account(parent_account, bitshares_instance=ctx.bitshares)

    # random password
    if not password:
        password = generate_password()

    print('password: {}\n'.format(password))
    # prints keys to stdout
    get_keys_from_password(account_name, password, ctx.bitshares)

    if not broadcast:
        ctx.log.info('Not broadcasting!')
        sys.exit(0)

    try:
        ctx.bitshares.create_account(
            account_name,
            registrar=parent_account,
            referrer=account['id'],
            referrer_percent=0,
            password=password,
            storekeys=True,
        )
    except MissingKeyError:
        ctx.log.critical('No key for {} in storage, use `uptick addkey` to add'.format(parent_account))
        sys.exit(1)


if __name__ == '__main__':
    main()
