#!/usr/bin/env python
import click

from bitsharesscripts.decorators import chain, common_options
from bitsharesscripts.functions import get_keys_from_password


@click.command()
@common_options
@chain
@click.argument('account_name')
@click.argument('password')
@click.pass_context
def main(ctx, account_name, password):
    """Generate private keys from password."""

    get_keys_from_password(account_name, password, ctx.bitshares)


if __name__ == '__main__':
    main()
