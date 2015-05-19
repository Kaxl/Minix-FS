#!/usr/bin/python
# -*- coding: utf-8 -*-
#Note : minix-fs types are little endian

from constantes import *
from minix_inode import *
from minix_superbloc import *
from bloc_device import *
from tester_answers import *

from bitarray import bitarray   # Library in C

class minix_file_system(object):
    """Class of the Minix File system."""

    def __init__(self,filename):
        """Initialization of a bitarray from the bitmap of inodes."""
        # Init of disk.
        self.disk = bloc_device(BLOCK_SIZE, filename)
        # Init of Minix Super block.
        self.super_bloc = minix_superbloc(self.disk)
        # Init of Inodes bitmap.
        self.inode_map = bitarray(endian='little')
        # Block one is for the superblock, so we start at 2.
        self.inode_map.frombytes(self.disk.read_bloc(MINIX_SUPER_BLOCK_NUM + 1,
                                                     self.super_bloc.s_imap_blocks))
        # Init of Blocks bitmap.
        self.zone_map = bitarray(endian='little')
        self.zone_map.frombytes(self.disk.read_bloc(MINIX_SUPER_BLOCK_NUM + self.super_bloc.s_imap_blocks + 1,
                                                    self.super_bloc.s_zmap_blocks))
        # Init of Inodes list.
        self.inodes_list = []
        # Find the first bloc.
        first_bloc_inodes = self.super_bloc.s_imap_blocks + self.super_bloc.s_zmap_blocks + MINIX_SUPER_BLOCK_NUM + 1

        # Inode 0 is null.
        self.inodes_list.append(minix_inode())
        # Run over each block of the Inode Table and insert them.
        for bloc_number in xrange(first_bloc_inodes, self.super_bloc.s_firstdatazone):
            bloc = self.disk.read_bloc(bloc_number)
            # Split the block 32 Bytes by 32 Bytes.
            for i in xrange (0, BLOCK_SIZE / INODE_SIZE):
                # Create the current inode.
                inode = minix_inode(bloc[i * INODE_SIZE:(i + 1) * INODE_SIZE],
                                    (bloc_number - first_bloc_inodes) * INODE_SIZE + i + 1)
                # Add the inode to the list.
                self.inodes_list.append(inode)

        return

    #return the first free inode number available
    #starting at 0 and upto s.n_inodes-1.
    #The bitmap ranges from index 0 to inod_num-1
    #Inode 0 is never and is always set.
    #according to the inodes bitmap
    def ialloc(self):
        print "IALLOC"
        for i in xrange(1, self.super_bloc.s_ninodes - 1):
            if  not (self.inode_map[i]):
                print "FOUND INODE : %s" % i
                return i

    #toggle an inode as available for the next ialloc()
    def ifree(self,inodnum):
        self.inode_map[inodnum] = 0
        return

    #return the first free bloc index in the volume. The bitmap
    #indicate the index from the bloc zone, add first_datazone then
    #to the bloc index
    def balloc(self):
        print "BALLOC"
        for i in xrange(0, self.super_bloc.s_nzones):
            if not (self.zone_map[i]):
                print "FOUND BLOC : %s" % i
                return i

    #toggle a bloc as available for the next balloc()
    #blocnum is an index in the zone_map
    def bfree(self,blocnum):
        self.zone_map[blocnum] = 0
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


