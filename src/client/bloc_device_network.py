#!/usr/bin/python
# -*- coding: utf-8 -*-

from constantes import *

import binascii
import socket
import struct
import random

class bloc_device_network(object):
    """Class to emulate a simple bloc device.
       Gets bloc units from a remote server or sends the bloc the server."""

    def __init__(self, blksize, server_address, server_port):
        """Initialisation of class."""
        self.block_size = blksize
        self.server_address = server_address
        self.server_port = server_port
        random.seed()
        return

    def read_bloc(self, block_num, num_of_block = 1):
        """Retreives a certain number of blocks from the server."""
        handle = random.randint(0, 4294967296)
        request = self.create_request(0, handle, block_num * self.block_size, num_of_block * self.block_size)
        addr = (self.server_address, self.server_port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(addr)
        sock.send(request)

        response = sock.recv(12)
        response = struct.unpack("!3I", response)

        if response[0] == 0x87878787 and response[2] == handle:
            if response[1] == 1:
                print("1")
            else:
                response = sock.recv(num_of_block * self.block_size)
                payload = struct.unpack("!" + str(num_of_block * self.block_size) + "s", response)

        sock.close()
        return payload

    def write_bloc(self, block_num, block):
        """Sends a certain number of blocks to write to the server."""
        handle = random.randint(0, 4294967296)
        request = self.create_request(1, handle, block_num * self.block_size, self.block_size, block)
        addr = (self.server_address, self.server_port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(addr)
        sock.send(request)

        response = sock.recv(12)
        response = struct.unpack("!3I", response)
        """
        if response[0] == 0x87878787 and response[2] == handle:
            if response[1] == 1:
                # error
            else:
                # no error
        """
        sock.close()
        return

    def create_request(self, read_write, handle, offset, length, payload = None):
        format = "!5I"
        if read_write == 0:
            format += "0s"
            payload = b""
        else:
            format += str(length) + "s"
        return struct.pack(format, 0x76767676, read_write, handle, offset, length, payload)
