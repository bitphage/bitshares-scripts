#!/usr/bin/env python


from pprint import pprint

import click
from bitshares.worker import Worker

from bitsharesscripts.decorators import chain, common_options


@click.command()
@common_options
@chain
@click.argument('worker_id')
@click.pass_context
def main(ctx, worker_id):
    """Show worker details."""

    worker = Worker(worker_id, bitshares_instance=ctx.bitshares)
    pprint(dict(worker))


if __name__ == '__main__':
    main()
