#!/usr/bin/python
# -*- coding: utf-8 -*-
# Note : minix-fs types are little endian

from constantes import *
from minix_inode import *
from minix_superbloc import *
from bloc_device import *
from tester_answers import *

from bitarray import bitarray  # Library in C


class minix_file_system(object):
    """Class of the Minix File system."""

    def __init__(self, filename):
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
            for i in xrange(0, BLOCK_SIZE / INODE_SIZE):
                # Create the current inode.
                inode = minix_inode(bloc[i * INODE_SIZE:(i + 1) * INODE_SIZE],
                                    (bloc_number - first_bloc_inodes) * INODE_SIZE + i + 1)
                # Add the inode to the list.
                self.inodes_list.append(inode)

        return

    # return the first free inode number available
    # starting at 0 and upto s.n_inodes-1.
    # The bitmap ranges from index 0 to inod_num-1
    # Inode 0 is never and is always set.
    # according to the inodes bitmap
    def ialloc(self):
        for i in xrange(0, self.super_bloc.s_ninodes):
            if not (self.inode_map[i]):
                self.ifree(i)
                return i

    # toggle an inode as available for the next ialloc()
    def ifree(self, inodnum):
        self.inode_map[inodnum] = not self.inode_map[inodnum]
        return

    # return the first free bloc index in the volume. The bitmap
    # indicate the index from the bloc zone, add first_datazone then
    # to the bloc index
    def balloc(self):
        for i in xrange(0, self.super_bloc.s_nzones):
            if not (self.zone_map[i]):
                self.bfree(i)
                return i + self.super_bloc.s_firstdatazone

    # toggle a bloc as available for the next balloc()
    # blocnum is an index in the zone_map
    def bfree(self, blocnum):
        self.zone_map[blocnum] = not self.zone_map[blocnum]
        return

    def bmap(self, inode, blk):
        # Cas 0 : direct block.
        # Get the number of direct bloc (element in zone != 0).
        # nb_direct_bloc = sum(bloc != 0 for bloc in inode.i_zone)
        nb_direct_bloc = len(inode.i_zone)
        if blk < nb_direct_bloc:
            return inode.i_zone[blk]

        # Subtract the number of directs blocks.
        blk -= nb_direct_bloc

        # Cas 1 : simple indirection.
        # With an indirect bloc, we can address BLOCK_SIZE / 2 direct block.
        # Each inode takes 32 bytes.
        if inode.i_indir_zone != 0 and blk < MINIX_ZONESZ:
            indirect_bloc = self.disk.read_bloc(inode.i_indir_zone)
            return struct.unpack('<H', indirect_bloc[blk * 2:blk * 2 + 2])[0]

        # Subtract the number of directs blocks we could have addressed with a simple redirection.
        blk -= BLOCK_SIZE / 2

        # Cas 2 : double indirection.
        # With an indirect bloc, we can address BLOCK_SIZE * BLOCK_SIZE direct block.
        if inode.i_dbl_indr_zone != 0 and blk < BLOCK_SIZE * BLOCK_SIZE:
            # Each value is on two bytes so we need to multiply by 2 the bloc number.
            # Load the indirect bloc.
            indirect_bloc = self.disk.read_bloc(inode.i_dbl_indr_zone)
            # Look for the number of the next indirect bloc.
            indirect2_bloc_nb = struct.unpack('<H', indirect_bloc[blk / MINIX_ZONESZ * 2:blk / MINIX_ZONESZ * 2 + 2])[0]
            # Load the double indirect bloc.
            indirect2_bloc = self.disk.read_bloc(indirect2_bloc_nb)
            return struct.unpack('<H', indirect2_bloc[blk % MINIX_ZONESZ * 2:blk % MINIX_ZONESZ * 2 + 2])[0]

        return 0

    # lookup for a name in a directory, and return its inode number, given inode directory dinode
    def lookup_entry(self, dinode, name):
        # Run over blocs of inode.
        for i in range(0, dinode.i_ino + dinode.i_size):
            bloc_number = self.bmap(dinode, i)
            data = self.disk.read_bloc(bloc_number)

            # Check each inodes to compare the name.
            for j in xrange(0, BLOCK_SIZE, INODE_SIZE):
                inode = data[j:j + INODE_SIZE]
                # Check if the name is in the inode.
                if name in inode:
                    return struct.unpack('<H', data[j:j + 2])[0]
        return

    # find an inode number according to its path
    # ex : '/usr/bin/cat'
    # only works with absolute paths

    def namei(self, path):
        return

    def ialloc_bloc(self, inode, blk):
        return

    # create a new entry in the node
    # name is an unicode string
    # parameters : directory inode, name, inode number
    def add_entry(self, dinode, name, new_node_num):
        return

    # delete an entry named "name"
    def del_entry(self, inode, name):
        return
