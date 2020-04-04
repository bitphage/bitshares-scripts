import logging
from functools import update_wrapper, wraps

import click
import yaml
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance

log = logging.getLogger(__name__)


def common_options(func):
    @click.option('-d', '--debug', default=False, is_flag=True, help='enable debug output')
    @click.option(
        '-c', '--config', type=click.File('r'), default='./config.yml', help='specify custom path for config file'
    )
    @click.pass_context
    @wraps(func)
    def wrapper(ctx, *args, **kwargs):
        ctx.obj = {}  # stub for uptick
        ctx.config = yaml.safe_load(kwargs.pop("config"))

        # create logger
        debug = kwargs.pop("debug")
        if debug is True:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
        ctx.log = log

        return func(*args, **kwargs)

    return wrapper


def chain(func):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        ctx.bitshares = BitShares(ctx.config['node_bts'], expiration=60)
        set_shared_bitshares_instance(ctx.bitshares)
        return ctx.invoke(func, *args, **kwargs)

    return update_wrapper(new_func, func)
