#!/usr/bin/env python3

import argparse
from codec import Codec


def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple compressor/decompressor for DRP file")

    parser.add_argument(
        'ifname',
        metavar='filename',
        action='store',
        help='file to compress (default) or extract (with -d)')

    parser.add_argument(
        '--decode', '-d',
        dest='is_bin',
        action='store_true',
        default=False,
        help='option to extract the selected file')

    return parser.parse_args()


def cli():
    args = parse_args()
    c = Codec(args)


if __name__ == '__main__':
    cli()
