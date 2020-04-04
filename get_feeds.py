#!/usr/bin/env python

import click
from bitshares.asset import Asset

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.argument('asset')
@click.pass_context
def main(ctx, asset):
    """Print current feeds for an asset."""
    asset = Asset(asset, bitshares_instance=ctx.bitshares)
    feeds = asset.feeds

    for feed in feeds:
        print('{}: {}'.format(feed['producer']['name'], feed['settlement_price']))


if __name__ == '__main__':
    main()
