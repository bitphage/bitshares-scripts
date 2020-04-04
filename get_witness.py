#!/usr/bin/env python

from pprint import pprint

import click
from bitshares.witness import Witness

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.argument('account')
@click.pass_context
def main(ctx, account):
    """Show witness object."""

    witness = Witness(account, bitshares_instance=ctx.bitshares)
    pprint(dict(witness))


if __name__ == '__main__':
    main()
