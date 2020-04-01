#!/usr/bin/env python

import argparse
import json
import logging
import sys
from pprint import pprint

import yaml
from bitsharesbase.account import PasswordKey, PublicKey

log = logging.getLogger(__name__)

roles = ['active', 'owner', 'memo']


def main():

    parser = argparse.ArgumentParser(description='Generate private keys from password', epilog='Report bugs to: ')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug output'),
    parser.add_argument('-c', '--config', default='./config.yml', help='specify custom path for config file')
    parser.add_argument('account')
    parser.add_argument('password')
    args = parser.parse_args()

    # create logger
    if args.debug == True:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # parse config
    with open(args.config, 'r') as ymlfile:
        conf = yaml.safe_load(ymlfile)

    for role in roles:
        key = PasswordKey(args.account, args.password, role=role)
        privkey = key.get_private_key()
        print('role: {}, key: {}'.format(role, str(privkey)))


if __name__ == '__main__':
    main()
