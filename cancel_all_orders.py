#!/usr/bin/env python

import sys

import click
from bitshares.account import Account
from bitshares.market import Market
from uptick.decorators import unlock

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@unlock
@click.option('--buy-only', default=False, is_flag=True, help='cancel only buy orders')
@click.option('--sell-only', default=False, is_flag=True, help='cancel only sell orders')
@click.option('--market', help='cancel orders only on specified market only, format is QUOTE/BASE')
@click.argument('account')
@click.pass_context
def main(ctx, buy_only, sell_only, market, account):
    """Cancel all orders of specified account.

    Optionally, you can select market like BTC/USD and choose buy/sell orders only
    """

    if buy_only and sell_only:
        ctx.log.critical('--buy-only and --sell-only are mutually exclusive')
        sys.exit(1)

    account = Account(account, blockchain_instance=ctx.bitshares)
    orders = [order for order in account.openorders if 'id' in order]

    if market:
        market = Market(market, blockchain_instance=ctx.bitshares)
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
    ctx.bitshares.cancel(ids, account=account)


if __name__ == '__main__':
    main()
