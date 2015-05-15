#!/usr/bin/python
# -*- coding: utf-8 -*-
#Note : minix-fs types are little endian

from constantes import *
from minix_inode import *
from minix_superbloc import *
from bloc_device import *

from bitarray import bitarray   # Library in C

class minix_file_system(object):
    """Class of the Minix File system."""

    def __init__(self,filename):
        """Initialization of a bitarray from the bitmap of inodes."""
        # Init of disk
        self.disk = bloc_device(BLOCK_SIZE, filename)
        # Init of Minix Super block
        self.super_bloc = minix_superbloc(self.disk)
        # Init of Inodes bitmap
        self.inode_map = bitarray(endian='little')
        # Block one is for the superblock, so we start at 2.
        self.inode_map.frombytes(self.disk.read_bloc(MINIX_SUPER_BLOCK_NUM + 1,
                                                     int(self.super_bloc.s_imap_blocks)))
        # Init of Blocks bitmap
        self.zone_map = bitarray(endian='little')
        self.zone_map.frombytes(self.disk.read_bloc(MINIX_SUPER_BLOCK_NUM + self.super_bloc.s_imap_blocks + 1,
                                                    self.super_bloc.s_zmap_blocks))
        # Init of Inodes list
        self.inodes_list = []
        # Append all inodes in the list.
        #for i in xrange(1, self.super_bloc.s_ninodes - 1):
        #for block in self.inode_map:
        #    print(block)
        #print self.inode_map.tobytes()
        #i = self.inode_map[0:256].tobytes()
        #inode = minix_inode(i)
        #print inode
        #for inode in self.inode_map.tobytes():
        #    print inode
            #i = minix_inode(inode)
            #print(i)
            #self.inodes_list.append(i)




            #current_inode = minix_inode(num=i)
            #self.inodes_list.append(current_inode)

        return

    #return the first free inode number available
    #starting at 0 and upto s.n_inodes-1.
    #The bitmap ranges from index 0 to inod_num-1
    #Inode 0 is never and is always set.
    #according to the inodes bitmap
    def ialloc(self):
        print "IALLOC"
        for i in xrange(0, self.super_bloc.s_ninodes - 1):
            if  not (self.inode_map[i]):
                print "FOUND : %s" %i
                return i

    #toggle an inode as available for the next ialloc()
    def ifree(self,inodnum):
        self.inode_map[inodnum] = 0
        return

    #return the first free bloc index in the volume. The bitmap
    #indicate the index from the bloc zone, add first_datazone then
    #to the bloc index
    def balloc(self):
        return

    #toggle a bloc as available for the next balloc()
    #blocnum is an index in the zone_map
    def bfree(self,blocnum):
        return

    def bmap(self,inode,blk):
        return

    #lookup for a name in a directory, and return its inode number, given inode directory dinode
    def lookup_entry(self,dinode,name):
        return

    #find an inode number according to its path
    #ex : '/usr/bin/cat'
    #only works with absolute paths

    def namei(self,path):
        return

    def ialloc_bloc(self,inode,blk):
        return

    #create a new entry in the node
    #name is an unicode string
    #parameters : directory inode, name, inode number
    def add_entry(self,dinode,name,new_node_num):
        return

    #delete an entry named "name"
    def del_entry(self,inode,name):
        return


