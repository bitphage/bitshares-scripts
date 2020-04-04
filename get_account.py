#!/usr/bin/env python

from pprint import pprint

import click
from bitshares.account import Account

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.argument('account')
@click.pass_context
def main(ctx, account):
    """Show account object."""
    account = Account(account, bitshares_instance=ctx.bitshares)
    pprint(dict(account))


if __name__ == '__main__':
    main()
