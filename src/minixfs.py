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
        # Init of disk
        self.disk = bloc_device(BLOCK_SIZE, filename)
        # Init of Minix Super block
        self.super_bloc = minix_superbloc(self.disk)
        # Init of Inodes bitmap
        self.inode_map = bitarray(endian='little')
        # Block one is for the superblock, so we start at 2.
        self.inode_map.frombytes(self.disk.read_bloc(MINIX_SUPER_BLOCK_NUM + 1,
                                                     self.super_bloc.s_imap_blocks))
        # Init of Blocks bitmap
        self.zone_map = bitarray(endian='little')
        self.zone_map.frombytes(self.disk.read_bloc(MINIX_SUPER_BLOCK_NUM + self.super_bloc.s_imap_blocks + 1,
                                                    self.super_bloc.s_zmap_blocks))
        # Init of Inodes list
        # TODO : parcourir la tables des inodes de 32 bits en 32 bits (INODE_SIZE)
        # Récupérer ses 32 bits et créer un inode.
        # Ajouter cet inode dans la liste des inodes.
        self.inodes_list = []
        inodes_table = []
        # Run over the inodes table and insert them.
        nb_bloc_inodes = (self.super_bloc.s_ninodes * INODE_SIZE) / BLOCK_SIZE
        # First block : Nb block IBitMap + DBitmap + superbloc (1) + 1 (because start at 0)
        first_bloc_inodes = self.super_bloc.s_imap_blocks + self.super_bloc.s_zmap_blocks + MINIX_SUPER_BLOCK_NUM + 1
        print "First bloc : %s" %first_bloc_inodes
        print "Nb bloc : %s" %nb_bloc_inodes
        print "Last bloc: %s" %self.super_bloc.s_firstdatazone

        # Inode 0 is null.
        self.inodes_list.append(minix_inode())
        print self.inodes_list
        # Run over each block of the Inode Table.
        for bloc_number in xrange(first_bloc_inodes, self.super_bloc.s_firstdatazone):
            bloc = self.disk.read_bloc(bloc_number)
            # Split the block 32 Bytes by 32 Bytes.
            for i in xrange (0, BLOCK_SIZE / INODE_SIZE):
                print "BLOC NUMBER : %s" %bloc_number
                print "Start : %s // End : %s" % (i * INODE_SIZE, (i + 1) * INODE_SIZE)
                print "Table %s" %bloc[i * INODE_SIZE:(i + 1) * INODE_SIZE]
                # Create the current inode.
                inode = minix_inode(bloc[i * INODE_SIZE:(i + 1) * INODE_SIZE],
                                    (bloc_number - first_bloc_inodes) * INODE_SIZE + i + 1)
                print inode
                # Add the inode to the list.
                self.inodes_list.append(inode)

        print "DONE"
        #print "INODELIST=%s" %self.inodes_list


#        print "Table %s" %inodes_table[32:64]
#        inode = minix_inode(inodes_table[32:64], 0)
#        print inode
        #for i in xrange(0, self.super_bloc.s_ninodes - 1):
        #    print "Start %s" % i * INODE_SIZE
        #    print "END %s" % (i + 1) * INODE_SIZE -1
        #    inode = minix_inode(inodes_table[i * INODE_SIZE:(i + 1) * INODE_SIZE - 1], num=i)
        #    print inode
        #    self.inodes_list.append(inode)



            #i = 0
            #while i < BLOCK_SIZE:
            #    inode = minix_inode(self.disk.read_bloc(bloc)[i:i + INODE_SIZE], bloc + i)
            #    self.inodes_list.append(inode)
            #    i += INODE_SIZE
        #print self.zone_map
        # Append all inodes in the list.
        #for i in xrange(1, self.super_bloc.s_ninodes - 1):
        #for block in self.inode_map:
        #    print(block)
        #print self.inode_map.tobytes()
        #i = self.inode_map[0:256].tobytes()
        #inode = minix_inode(self.inode_map[0:256])
        #self.inode_list.append(inode)
        ##print inode
        #for i in self.inode_map:
        #    if i:
        #        inode = minix_inode(

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
        return

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


