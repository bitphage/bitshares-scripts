#!/usr/bin/env python

from typing import Dict

import click
from bitshares.account import Account

from bitsharesscripts.decorators import chain, common_options
from bitsharesscripts.functions import transform_asset


@click.command()
@common_options
@chain
@click.pass_context
def main(ctx):
    """Summarize all assets on all accounts and show BTC equivalent."""

    sum_balances: Dict[str, float] = {}

    for acc in ctx.config['my_accounts']:
        account = Account(acc, bitshares_instance=ctx.bitshares)

        # Avail balances
        for i in account.balances:
            asset = i['symbol']
            sum_balances[asset] = sum_balances.setdefault(asset, 0) + i['amount']

        # Balance in orders
        for order in account.openorders:
            asset = order['for_sale']['symbol']
            sum_balances[asset] = sum_balances.setdefault(asset, 0) + order['for_sale']['amount']

        # Margin positions
        for asset, details in account.callpositions.items():
            sum_balances[asset] = sum_balances.setdefault(asset, 0) - details['debt']['amount']

            asset = details['collateral']['asset']['symbol']
            sum_balances[asset] = sum_balances.setdefault(asset, 0) + details['collateral']['amount']

    for asset, amount in sum_balances.items():
        ctx.log.debug('Total: {} {}'.format(asset, amount))

    for from_asset, to_asset in ctx.config['transform_assets'].items():
        ctx.log.debug('Transforming {} to {}'.format(from_asset, to_asset))
        sum_balances = transform_asset(ctx.bitshares, sum_balances, from_asset, to_asset)

    for asset, amount in sum_balances.items():
        if amount > 0 and asset != ctx.config['btc_asset']:
            ctx.log.info('Using direct conversion {:.8f} {} -> {}'.format(amount, asset, ctx.config['btc_asset']))
            sum_balances = transform_asset(ctx.bitshares, sum_balances, asset, ctx.config['btc_asset'])

    print('Accounts value in {}: {:.8f}'.format(ctx.config['btc_asset'], sum_balances[ctx.config['btc_asset']]))


if __name__ == '__main__':
    main()
