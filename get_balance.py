#!/usr/bin/env python

from collections import Counter
from typing import Counter as TCounter

import click
from bitshares.account import Account

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.argument('account')
@click.pass_context
def main(ctx, account):
    """Show account balances (avail + orders balance)"""

    sum_balances: TCounter[str] = Counter()

    account = Account(account, bitshares_instance=ctx.bitshares)

    for i in account.balances:
        sum_balances[i['symbol']] += i['amount']

    for order in account.openorders:
        asset = order['for_sale']['symbol']
        sum_balances[asset] += order['for_sale']['amount']

    for key in sum_balances:
        print('{}: {:.8f}'.format(key, sum_balances[key]))


if __name__ == '__main__':
    main()
