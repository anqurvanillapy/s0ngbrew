#!/usr/bin/env python3

import io
import zlib
from struct import pack, unpack


class Codec(object):
    """\
    Main codec for DRP.
    """
    def __init__(self, ifname='', ofname='', is_bin=True):
        self.ifname = ifname
        self.is_bin = is_bin
        self.iofunc = (self.encode, self.decode)[self.is_bin]

    def run(self):
        """\
        Run the codec and write the output file.
        """
        with open(self.ifname, ('r', 'rb')[self.is_bin]) as f:
            self.iofunc(f)

    def encode(self, f):
        """\
        Encode DRP
        """
        print('encode', f.read())

    def decode(self, f):
        """\
        Decode DRP
        """
        print('decode', f.read())
