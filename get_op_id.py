#!/usr/bin/env python

from pprint import pprint

from bitsharesbase import operationids


def main():
    # Just print operations with corresponding ids
    pprint(operationids.operations)


if __name__ == '__main__':
    main()
