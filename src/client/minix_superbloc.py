#!/usr/bin/python
# -*- coding: utf-8 -*-
from constantes import *

class minix_superbloc(object):
    """Class superbloc."""

    def __init__(self, bloc_device):
        """
        Initialisation of the superblock.
        System is always in little endian (value of s_magic not checked).

        :param bloc_device: the block containing the superblock.
        :return:
        """

        # Get the first bloc (superblock).
        block = bloc_device.read_bloc(MINIX_SUPER_BLOCK_NUM)
        # Get the values for each field.
        # WARNING : Little endian, octect need to be interverted.
        # struc.unpack('<H', block) extract the value in little endian.
        # '<H' is 2 bytes / '<I' is 4 bytes
        # struc.unpack always return a tuples.
        # To get the value, use [0].

        self.s_ninodes = struct.unpack('<H', block[0:2])[0]
        self.s_nzones = struct.unpack('<H', block[2:4])[0]
        self.s_imap_blocks = struct.unpack('<H', block[4:6])[0]
        self.s_zmap_blocks = struct.unpack('<H', block[6:8])[0]
        self.s_firstdatazone = struct.unpack('<H', block[8:10])[0]
        self.s_log_zone_size = struct.unpack('<H', block[10:12])[0]
        self.s_max_size = struct.unpack('<I', block[12:16])[0]
        self.s_magic = struct.unpack('<H', block[16:18])[0]
        self.s_state = struct.unpack('<H', block[18:20])[0]

        return
