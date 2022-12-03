#!/usr/bin/env python

from pprint import pprint

import click
from bitshares.asset import Asset

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.argument('asset')
@click.pass_context
def main(ctx, asset):
    """Get margin positions for an asset.

    TODO: this script is unfinished
    """

    asset = Asset(asset)
    orders = asset.get_call_orders(limit=2)

    for order in orders:
        pprint(order)


if __name__ == '__main__':
    main()
