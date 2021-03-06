#!/usr/bin/python
# -*- coding: utf-8 -*-
# Minix est little endian par défaut.
from constantes import *

class minix_inode(object):
    """Class of a minix inode."""

    def __init__(self,raw_inode=None,num=0,mode=0,uid=0,size=0,time=0,gid=0,nlinks=0,zone=[],indir_zone=0,dblr_indir_zone=0):
        """
        Initialization of a minix inode with the given values.
        :param raw_inode:       data
        :param num:             number of inode
        :param mode:            file access
        :param uid:             mode (user id = 0 => root)
        :param size:            size of file in bytes
        :param time:            time since 1/1/1970
        :param gid:             group id
        :param nlinks:          number of paths pointing to this inode
        :param zone:            address logique of blocks direct
        :param indir_zone:      indirect block
        :param dblr_indir_zone: double indirect block
        :return:
        """
        if raw_inode is None:
            self.i_ino = num
            self.i_mode = mode
            self.i_uid = uid
            self.i_size = size
            self.i_time = time
            self.i_gid = gid
            self.i_nlinks = nlinks
            self.i_zone = zone
            self.i_indir_zone = indir_zone
            self.i_dbl_indr_zone = dblr_indir_zone
        else:
            # If raw_inode is provided, parse it and affect it to each field.
            self.i_ino = num
            self.i_mode = struct.unpack('<H', raw_inode[0:2])[0]
            self.i_uid = struct.unpack('<H', raw_inode[2:4])[0]
            self.i_size = struct.unpack('<I', raw_inode[4:8])[0]
            self.i_time = struct.unpack('<I', raw_inode[8:12])[0]
            self.i_gid = struct.unpack('<B', raw_inode[12:13])[0]
            self.i_nlinks = struct.unpack('<B', raw_inode[13:14])[0]
            self.i_zone = [0] * 7
            self.i_zone[0] = struct.unpack('<H', raw_inode[14:16])[0]
            self.i_zone[1] = struct.unpack('<H', raw_inode[16:18])[0]
            self.i_zone[2] = struct.unpack('<H', raw_inode[18:20])[0]
            self.i_zone[3] = struct.unpack('<H', raw_inode[20:22])[0]
            self.i_zone[4] = struct.unpack('<H', raw_inode[22:24])[0]
            self.i_zone[5] = struct.unpack('<H', raw_inode[24:26])[0]
            self.i_zone[6] = struct.unpack('<H', raw_inode[26:28])[0]
            self.i_indir_zone = struct.unpack('<H', raw_inode[28:30])[0]
            self.i_dbl_indr_zone = struct.unpack('<H', raw_inode[30:32])[0]


    def __eq__(self, other):
        if isinstance(other, minix_inode):
            return self.i_ino == other.i_ino and \
                   self.i_mode == other.i_mode and \
                   self.i_uid == other.i_uid and \
                   self.i_size == other.i_size and \
                   self.i_time == other.i_time and \
                   self.i_gid == other.i_gid and \
                   self.i_nlinks == other.i_nlinks and \
                   self.i_zone == other.i_zone and \
                   self.i_indir_zone == other.i_indir_zone and \
                   self.i_dbl_indr_zone == other.i_dbl_indr_zone

    def __repr__(self):
        return "minix_inode("+"num="+str(self.i_ino) +\
                              ",mode="+str(self.i_mode) +\
                              ",uid="+str(self.i_uid) +\
                              ",size="+str(self.i_size) +\
                              ",time="+str(self.i_time) +\
                              ",gid="+str(self.i_gid) +\
                              ",nlinks="+str(self.i_nlinks) +\
                              ",zone="+str(eval(repr(self.i_zone))) +\
                              ",indir_zone="+str(self.i_indir_zone) +\
                              ",dblr_indir_zone="+str(self.i_dbl_indr_zone) +\
                              ")"
