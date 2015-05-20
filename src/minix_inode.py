#!/usr/bin/python
# -*- coding: utf-8 -*-
# Minix est little endian par défaut.
from constantes import *

class minix_inode(object):
    #inodes can be initializted from given values or from raw bytes contents coming from the device
    def __init__(self,raw_inode=None,num=0,mode=0,uid=0,size=0,time=0,gid=0,nlinks=0,zone=[],indir_zone=0,dblr_indir_zone=0):
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
            #print "\nINODE"
            #print "Len : %s" %len(raw_inode)
            #print raw_inode
            self.i_ino = num
            #print "i_ino : %s" % self.i_ino
            self.i_mode = struct.unpack('<H', raw_inode[0:2])[0]
            #print "i_mode : %s" % self.i_mode
            self.i_uid = struct.unpack('<H', raw_inode[2:4])[0]
            #print "i_uid : %s" % self.i_uid
            self.i_size = struct.unpack('<I', raw_inode[4:8])[0]
            #print "i_size : %s" % self.i_size
            self.i_time = struct.unpack('<I', raw_inode[8:12])[0]
            #print "i_time : %s" % self.i_time
            self.i_gid = struct.unpack('<B', raw_inode[12:13])[0]
            #print "i_gid : %s" % self.i_gid
            self.i_nlinks = struct.unpack('<B', raw_inode[13:14])[0]
            #print "i_nlinks : %s" % self.i_nlinks
            self.i_zone = [0] * 7
            self.i_zone[0] = struct.unpack('<H', raw_inode[14:16])[0]
            self.i_zone[1] = struct.unpack('<H', raw_inode[16:18])[0]
            self.i_zone[2] = struct.unpack('<H', raw_inode[18:20])[0]
            self.i_zone[3] = struct.unpack('<H', raw_inode[20:22])[0]
            self.i_zone[4] = struct.unpack('<H', raw_inode[22:24])[0]
            self.i_zone[5] = struct.unpack('<H', raw_inode[24:26])[0]
            self.i_zone[6] = struct.unpack('<H', raw_inode[26:28])[0]
            #print "i_zone : %s" % self.i_zone
            self.i_indir_zone = struct.unpack('<H', raw_inode[28:30])[0]
            #print "i_indir_zone : %s" % self.i_indir_zone
            self.i_dbl_indr_zone = struct.unpack('<H', raw_inode[30:32])[0]
            #print "i_dbl_indr_zone : %s" % self.i_dbl_indr_zone


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
