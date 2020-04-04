#!/usr/bin/env python

import sys

import click
from bitshares.account import Account

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.pass_context
def main(ctx):
    """Show ids of accounts defined in `my_accounts` config var.

    The format is suitable for BITSHARESD_TRACK_ACCOUNTS= env variable to use in docker-compose.yml for running docker
    image bitshares/bitshares-core:latest
    """

    if not ctx.config['my_accounts']:
        ctx.log.critical('You need to list your accounts in "my_accounts" config variable')
        sys.exit(1)

    ids = ''
    for account_name in ctx.config['my_accounts']:
        account = Account(account_name, bitshares_instance=ctx.bitshares)
        ids += '"{}" '.format((account['id']))

    print(ids)


if __name__ == '__main__':
    main()
