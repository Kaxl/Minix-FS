#!/usr/bin/python
# -*- coding: utf-8 -*-
from constantes import *

import binascii

class minix_superbloc(object):
    """Class superbloc."""

    # OK, according to tester.py.
    def __init__(self, bloc_device):
        """Initialisation of the superblock.
        System is always in little endian (value of s_magic not checked)."""
        # Get the first bloc (superblock).
        block = bloc_device.read_bloc(MINIX_SUPER_BLOCK_NUM)
        # Get the values for each field.
        # WARNING : Little endian, octect need to be interverted.
        # struc.unpack('<H', block) extract the value in little endian.
        # '<H' is 2 bytes / '<I' is 4 bytes
        # struc.unpack always return a tuples.
        # To get the value, use [0].

        #print "\nSUPERBLOCK"
        self.s_ninodes = struct.unpack('<H', block[0:2])[0]
        #print "s_ninodes : %s" % self.s_ninodes
        self.s_nzones = struct.unpack('<H', block[2:4])[0]
        #print "s_nzones : %s" % self.s_nzones
        self.s_imap_blocks = struct.unpack('<H', block[4:6])[0]
        #print "s_imap_blocks : %s" % self.s_imap_blocks
        self.s_zmap_blocks = struct.unpack('<H', block[6:8])[0]
        #print "s_zmap_blocks : %s" % self.s_zmap_blocks
        self.s_firstdatazone = struct.unpack('<H', block[8:10])[0]
        #print "s_firstdatazone : %s" % self.s_firstdatazone
        self.s_log_zone_size = struct.unpack('<H', block[10:12])[0]
        #print "s_log_zone_size : %s" % self.s_log_zone_size
        self.s_max_size = struct.unpack('<I', block[12:16])[0]
        #print "s_max_size : %s" % self.s_max_size
        self.s_magic = struct.unpack('<H', block[16:18])[0]
        #print "s_magic : %s" % self.s_magic
        self.s_state = struct.unpack('<H', block[18:20])[0]
        #print "s_state : %s" % self.s_state

        return
