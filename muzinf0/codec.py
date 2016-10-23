#!/usr/bin/env python3

import os
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
        with open(self.ifname, 'rb') as f:
            self.iofunc(f)

    def encode(self, f):
        """\
        Encode DRP: Boilderplate header and XML compression
        """
        rxml_data = f.read()
        bxml_data = zlib.compress(rxml_data)
        bxmls, rxmls = len(bxml_data) + 4, len(rxml_data) # 4 for rxmls
        checksum = rxmls
        unknown_margin = (0x20000001, 0x00000290, 0x00010001, 0)
        quadup = lambda x: (x, x, x, x)
        align = lambda x: x * b'\x00'

        with open(self.ofname, 'wb') as of:
            unknown, filecount = 2, 1
            of.seek(0x14)
            of.write(pack('>HH', unknown, filecount))
            of.seek(0x60)
            # Notice: the original musicInfo.drp stores the filename
            # `musicinfo_db`, which might be game-specific
            of.write(bytes(os.path.splitext(self.ifname)[0].encode('ascii')))
            of.seek(0xa0)
            of.write(pack('>8I', *unknown_margin, *quadup(bxmls)))
            of.write(pack('>I', checksum))
            of.write(bxml_data)

            remain = of.tell() % 0x10
            if remain:
                of.write(align(0x10 - remain))
                
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
        bxml_data = f.read(bxmls - 4) # rxmls is an unsigned integer

        if bxmls > 80:
            bxml_data = zlib.decompress(bxml_data) # no Unix EOF (\n)

        if len(bxml_data) != rxmls:
            raise ChecksumError('Checksum failed, file might be broken')

        with open(self.ofname, 'wb') as of:
            of.write(bxml_data)
