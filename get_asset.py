#!/usr/bin/env python

from pprint import pprint

import click
from bitshares.asset import Asset

from bitsharesscripts.decorators import chain, common_options
from bitsharesscripts.functions import raw_to_decimal


@click.command()
@common_options
@chain
@click.option('--raw', is_flag=True, default=False, help='show raw asset data')
@click.argument('asset')
@click.pass_context
def main(ctx, raw, asset):
    """Get asset info."""

    asset = Asset(asset, full=True, bitshares_instance=ctx.bitshares)

    if raw:
        pprint(dict(asset))
        return

    print('id: {}'.format(asset['id']))
    supply = raw_to_decimal(asset['dynamic_asset_data']['current_supply'], asset['precision'])
    print('supply: {} {}'.format(supply, asset['symbol']))

    if asset.is_bitasset:
        feed = asset.feed
        print('MCR: {}'.format(feed['maintenance_collateral_ratio']))
        print('MSSR: {}'.format(feed['maximum_short_squeeze_ratio']))
        print('Settlement: {}'.format(feed['settlement_price']))
        print('CER: {}'.format(feed['core_exchange_rate']))


if __name__ == '__main__':
    main()
