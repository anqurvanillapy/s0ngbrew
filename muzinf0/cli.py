#!/usr/bin/env python3

import argparse
from codec import Codec


def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple hack for musicInfo.drp")

    parser.add_argument(
        'ifname',
        metavar='infile',
        action='store',
        help='file to compress (default) or extract (with -d)')

    parser.add_argument(
        'ofname',
        metavar='outfile',
        action='store',
        help='output filename')

    parser.add_argument(
        '--decode', '-d',
        dest='is_bin',
        action='store_true',
        default=False,
        help='option to extract the selected file')

    return parser.parse_args()


def cli():
    """\
    Codec CLI for instant usage: Read and write.
    """
    argv = parse_args()
    c = Codec(**vars(argv))
    c.run()


if __name__ == '__main__':
    cli()
