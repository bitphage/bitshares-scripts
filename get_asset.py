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
    """Get asset info."""

    asset = Asset(asset, full=True, bitshares_instance=ctx.bitshares)
    pprint(dict(asset))


if __name__ == '__main__':
    main()
