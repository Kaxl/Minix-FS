#!/usr/bin/python
# -*- coding: utf-8 -*-

from constantes import *

import binascii

class bloc_device(object):
    """Class to emulate a simple bloc device.
       Reads and writes into the file by block units."""

    def __init__(self, blksize, pathname):
        """Initialisation of class."""
        self.block_size = blksize
        self.filename = pathname
        return

    # OK, according to tester.py
    def read_bloc(self, block_num, num_of_block=1):
        """Read a certain number of blocks.
           Get to the right position in the file and
           return the desired number of blocks."""
        with open(self.filename, 'rb') as f:
            f.seek(0, 0)    # Go to the beginning of the file to be sure.
            f.seek(block_num * self.block_size, 0) # Go to the right offset.
            print "READ Bloc %s" % block_num
            print "Position %s" % (block_num * self.block_size)
            blocka = f.read(self.block_size * num_of_block)
            print binascii.hexlify(blocka)
            #return f.read(self.block_size * num_of_block)
            return blocka

    # OK, according to tester.py
    def write_bloc(self, block_num, block):
        """Write a certain number of blocks.
           Get to the right position (block number) and
           writes the block."""
        with open(self.filename, 'r+b') as f:
            f.seek(0, 0)
            f.seek(block_num * self.block_size, 0) # Go to the right offset.
            print "WRITE Bloc %s" % block_num
            print "Position %s" % (block_num * self.block_size)
            print binascii.hexlify(block)
            f.write(block)
            # What happens if size of block is not equal to block_size ??? write 0 at the end to complete ?

            # Can we write multiple block ?
            # Do I need to clear the block before writing the new one ?
            # -> If the block is smaller, old data will still be present ?
        return
