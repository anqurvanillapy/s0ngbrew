#!/usr/bin/env python3

import io


class Codec(object):
    """Main codec for DRP"""
    def __init__(self, args):
        self.ifname = args.ifname
        self.is_bin = args.is_bin
        self.iofunc = (self.encode, self.decode)[self.is_bin]

        self.file_entry(self.ifname, self.is_bin)

    def file_entry(self, fn, is_bin):
        with open(fn, ('r', 'rb')[is_bin]) as filehandle:
            self.iofunc(filehandle)

    def encode(self, fh):
        print('encode', fh.read())

    def decode(self, fh):
        print('decode', fh.read())
