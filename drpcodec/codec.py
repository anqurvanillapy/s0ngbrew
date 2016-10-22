#!/usr/bin/env python3

import zlib
from struct import pack, unpack


class FileCountError(Exception):
    pass


class ChecksumError(Exception):
    pass


class Codec(object):
    """\
    Main codec for DRP.
    """
    def __init__(self, ifname='', ofname='', is_bin=True):
        self.ifname = ifname
        self.ofname = ofname
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
        Encode DRP: Boilderplate header and XML compression
        """
        return

    def decode(self, f):
        """\
        Decode DRP: Decompress XML data
        """
        f.seek(0x14)
        unknown, filecount = unpack('>HH', f.read(4))

        if filecount != 1:
            raise FileCountError('Not a single XML compressed file')

        f.seek(0x60)
        fname = f.read(0x40).split(b'\x00')[0]
        f.seek(0x10, 1)
        # bxmls: binary XML size (zlib compressed), rxmls: Raw XML size
        # the 4 bxmls are duplicate, and rxmls is for checksum
        bxmls, bxmls2, bxmls3, bxmls4, rxmls = unpack('>5I', f.read(4 * 5))
        bxml_data = f.read(bxmls2 - 4) # rxmls is an unsigned integer

        print(bxmls, rxmls)

        if bxmls > 80:
            bxml_data = zlib.decompress(bxml_data) # no Unix EOF (\n)

        if len(bxml_data) != rxmls:
            raise ChecksumError('Checksum failed, file might be broken')

        self.write(bxml_data.decode('utf-8'))

    def write(self, buf):
        """\
        Write XML/DRP
        """
        with open(self.ofname, ('wb', 'w')[self.is_bin]) as f:
            f.write(buf)
