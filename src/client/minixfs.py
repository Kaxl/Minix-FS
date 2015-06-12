#!/usr/bin/python
# -*- coding: utf-8 -*-
# Note : minix-fs types are little endian

from constantes import *
from minix_inode import *
from minix_superbloc import *
from bloc_device import *
from bloc_device_network import *
from tester_answers import *

from bitarray import bitarray  # Library in C


class minix_file_system(object):
    """Class of the Minix File system."""

    def __init__(self, source=None, port=None):
        """
        Initialization of a bitarray from the bitmap of inodes.

        :param source:  the filename with the image of the source address depending
                        on if we are on the network or not.
        :param port:    the port for the network connection.
        :return:
        """

        # Init of disk.
        # Depending on if we got an ip and a port, we initiate a bloc_device_network.
        if source and port:
            self.disk = bloc_device_network(BLOCK_SIZE, source, port)
        else:
            self.disk = bloc_device(BLOCK_SIZE, source)

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

    def ialloc(self):
        """
        Return the first free inode number available
        starting at 0 and upto s.n_inodes - 1.
        Reminder : Inode 0 is never used and always set,
        according to the inodes bitmap.

        :return:
        """
        for i in xrange(0, self.super_bloc.s_ninodes):
            if not (self.inode_map[i]):
                self.inode_map[i] = True
                self.inodes_list[i] = minix_inode(num=i)
                return i

    def ifree(self, inodnum):
        """
        Toogle an inode as available for the next ialloc().

        :param inodnum: the inode to free.
        :return:
        """
        self.inode_map[inodnum] = False
        return

    def balloc(self):
        """
        Return the first free bloc index in the volume.
        The bitmap indicate the indx from the bloc zone,
        add first_datazone then to the bloc index.

        :return:
        """
        for i in xrange(0, self.super_bloc.s_nzones):
            if not (self.zone_map[i]):
                self.zone_map[i] = True
                return i + self.super_bloc.s_firstdatazone

    def bfree(self, blocnum):
        """
        Toogle a bloc as available for the next balloc()

        :param blocnum: index in the zone map.
        :return:
        """
        self.zone_map[blocnum] = False
        return

    def bmap(self, inode, blk):
        """
        Make the link between a bloc number of a file
        with a bloc number of the disk.

        :param inode:   inode to check.
        :param blk:     bloc number.
        :return:
        """
        # Case 0 : direct block.
        # Get the number of direct bloc (element in zone != 0).
        # nb_direct_bloc = sum(bloc != 0 for bloc in inode.i_zone)
        nb_direct_bloc = len(inode.i_zone)
        if blk < nb_direct_bloc:
            return inode.i_zone[blk]

        # Subtract the number of directs blocks.
        blk -= nb_direct_bloc

        # Case 1 : simple indirection.
        # With an indirect bloc, we can address BLOCK_SIZE / 2 direct block.
        # Each inode takes 32 bytes.
        if inode.i_indir_zone != 0 and blk < MINIX_ZONESZ:
            indirect_bloc = self.disk.read_bloc(inode.i_indir_zone)
            return struct.unpack('<H', indirect_bloc[blk * 2:blk * 2 + 2])[0]

        # Subtract the number of directs blocks we could have addressed with a simple redirection.
        blk -= MINIX_ZONESZ

        # Case 2 : double indirection.
        # With an indirect block, we can address BLOCK_SIZE * BLOCK_SIZE direct block.
        if inode.i_dbl_indr_zone != 0 and blk < MINIX_ZONESZ * MINIX_ZONESZ:
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
        blk = 0
        # Run over blocks of inode.
        while self.bmap(dinode, blk):
            bloc_number = self.bmap(dinode, blk)
            data = self.disk.read_bloc(bloc_number)
            blk += 1

            # Check each inodes to compare the name.
            for i in xrange(0, BLOCK_SIZE, DIRSIZE):
                inode = data[i:i + DIRSIZE]
                # Check if the name is in the inode.
                if name in inode:
                    return struct.unpack('<H', data[i:i + 2])[0]

    # find an inode number according to its path
    # ex : '/usr/bin/cat'
    # only works with absolute paths
    def namei(self, path):
        # Get the first inode (root)
        inode = self.inodes_list[MINIX_ROOT_INO].i_ino
        # We don't need the first element of the list because we already got the first inode (root).
        path_list = path.split('/')[1:]
        for d in path_list:
            # Get the inode of the next element of the path.
            inode = self.lookup_entry(self.inodes_list[inode], d)

        return inode

    # Add a new empty block in an inode.
    def ialloc_bloc(self, inode, blk):
        # Cas 0 : direct block.
        nb_direct_bloc = len(inode.i_zone)
        if blk < nb_direct_bloc:
            if not inode.i_zone[blk]:
                inode.i_zone[blk] = self.balloc()
            return inode.i_zone[blk]

        # Subtract the number of directs blocks.
        blk -= nb_direct_bloc

        # Case 1 : simple indirection.
        if blk < MINIX_ZONESZ:
            if not inode.i_indir_zone:
                inode.i_indir_zone = self.balloc()
                # Initialize the bloc with \x00.
                self.disk.write_bloc(inode.i_indir_zone, bytearray("".ljust(BLOCK_SIZE, '\x00')))

            indirect_bloc = self.disk.read_bloc(inode.i_indir_zone)
            if not indirect_bloc[blk]:
                indirect_bloc[blk] = self.balloc()
                # Write a new bloc.
                self.disk.write_bloc(indirect_bloc, inode.i_indir_zone)
            return indirect_bloc[blk]

        blk -= MINIX_ZONESZ

        # Case 2 : double indirections.
        if blk < MINIX_ZONESZ * MINIX_ZONESZ:
            # If double indirect bloc not allocated, allocate it.
            if not inode.i_dbl_indr_zone:
                inode.i_dbl_indr_zone = self.balloc()
                # Create a new bloc (fill with \x00)
                self.disk.write_bloc(inode.i_dbl_indr_zone, bytearray("".ljust(BLOCK_SIZE, '\x00')))
                return inode.i_dbl_indr_zone

            # Load the indirect bloc.
            indirect_bloc = self.disk.read_bloc(inode.i_dbl_indr_zone)
            # Look for the number of the next indirect bloc.
            indirect2_bloc_nb = struct.unpack('<H', indirect_bloc[blk / MINIX_ZONESZ * 2:blk / MINIX_ZONESZ * 2 + 2])[0]
            # Load the double indirect bloc.
            indirect2_bloc = self.disk.read_bloc(indirect2_bloc_nb)

            # If not loaded, create a new one.
            if not indirect2_bloc[blk]:
                indirect2_bloc[blk] = self.balloc()
                # Create a new bloc (fill with \x00)
                self.disk.write_bloc(indirect2_bloc_nb, bytearray("".ljust(BLOCK_SIZE, '\x00')))
                return indirect2_bloc_nb[blk]

    # create a new entry in the node
    # name is an unicode string
    # parameters : directory inode, name, inode number
    def add_entry(self, dinode, name, new_node_num):
        blk = 0
        # While bmap return something, we check it.
        while self.bmap(dinode, blk):
            # Get the block number and load the block.
            bloc_number = self.bmap(dinode, blk)
            bloc = bytearray(self.disk.read_bloc(bloc_number))
            blk += 1
            # Run over the block.
            for offset in range(0, BLOCK_SIZE, DIRSIZE):
                if not struct.unpack_from("<H", bloc, offset)[0]:
                    # Add the new inode number.
                    struct.pack_into('H', bloc, offset, new_node_num)
                    # Add the name.
                    bloc[offset + 2:offset + DIRSIZE] = name.ljust(DIRSIZE - 2, '\x00')
                    # Increase the size.
                    dinode.i_size += DIRSIZE
                    # Write the bloc.
                    self.disk.write_bloc(bloc_number, bloc)
                    return

        # If we arrive here, we need to allocate a new bloc.
        bloc = bytearray("".ljust(BLOCK_SIZE, '\x00'))
        # Add the new inode number.
        struct.pack_into('H', bloc, 0, new_node_num)
        # Add the name.
        bloc[2:DIRSIZE] = name.ljust(DIRSIZE - 2, '\x00')
        # Increase the size.
        dinode.i_size += DIRSIZE
        self.disk.write_bloc(self.ialloc_bloc(dinode, blk), bloc)
        return

    #delete an entry named "name"
    def del_entry(self, inode, name):
        # Empty the name.
        name = name.ljust(DIRSIZE - 2, '\x00')

        blk = 0
        # While bmap return something, we check it.
        while self.bmap(inode, blk):
            # Get the block number and load the block.
            #bloc_number = self.bmap(inode, i)
            bloc_number = self.bmap(inode, blk)
            bloc = bytearray(self.disk.read_bloc(bloc_number))

            # Run over entries of block.
            for offset in xrange(0, BLOCK_SIZE, DIRSIZE):
                if (struct.unpack_from("<14s", bloc, 2 + offset)[0] == name):
                    # Remove the entry en free the inode.
                    bloc[offset:offset + 2] = "".ljust(2, '\x00')
                    #self.ifree(inode)
                    self.disk.write_bloc(bloc_number, bloc)
                    inode.i_size -= DIRSIZE

                    # Check if block is empty and free it if so.
                    if self.disk.read_bloc(bloc_number) == "".ljust(BLOCK_SIZE, '\x00'):
                        self.bfree(bloc_number)

                    return
        return

