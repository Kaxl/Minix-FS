#!/usr/bin/python
# -*- coding: utf-8 -*-

from constantes import *

import binascii
import socket
import struct
import random


class bloc_device(object):
    """
    Class to emulate a simple bloc device.
    Reads and writes into the file by block units.

    This class doesn't work with network.
    It is just used with images.
    """

    def __init__(self, blksize, pathname):
        """
        Initialization of class.

        :param blksize:     the size of a block.
        :param pathname:    the image to read / write.
        :return:
        """
        self.block_size = blksize
        self.filename = pathname
        return

###############################################################################
    def read_bloc(self, block_num, num_of_block=1):
        """
        Read a certain number of blocks.
        Get to the right position in the file and
        return the desired number of blocks.

        :param block_num:       the block number to read.
        :param num_of_block:    the number of block to read.
        :return:                return the block.
        """
        with open(self.filename, 'rb') as f:
            f.seek(0, 0)    # Go to the beginning of the file to be sure.
            f.seek(block_num * self.block_size, 0) # Go to the right offset.
            return f.read(self.block_size * num_of_block)

###############################################################################
    def write_bloc(self, block_num, block):
        """
        Write a certain number of blocks.
        Get to the right position (block number) and
        writes the block.

        :param block_num:   the block number to write.
        :param block:       the content of the block.
        :return:
        """
        with open(self.filename, 'r+b') as f:
            f.seek(0, 0)
            f.seek(block_num * self.block_size, 0) # Go to the right offset.
            f.write(block)
        return
