#!/usr/bin/env python

import sys
from collections import Counter
from typing import Counter as TCounter

import click
from bitshares.account import Account

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.pass_context
def main(ctx):
    """Show multiple accounts balances sum (avail + orders balance)"""

    if not ctx.config['my_accounts']:
        ctx.log.critical('You need to list your accounts in "my_accounts" config variable')
        sys.exit(1)

    sum_balances: TCounter[str] = Counter()

    for account_name in ctx.config['my_accounts']:
        account = Account(account_name, bitshares_instance=ctx.bitshares)

        for i in account.balances:
            sum_balances[i['symbol']] += i['amount']

        for order in account.openorders:
            asset = order['for_sale']['symbol']
            sum_balances[asset] += order['for_sale']['amount']

    for key in sum_balances:
        print('{}: {:.8f}'.format(key, sum_balances[key]))


if __name__ == '__main__':
    main()
