import sys
from socket import *
import os

def put_cmd(filename, sock, buff_size):
    """ Takes filename and uploads by reading chunks and sending them over the open socket"""
    if not os.path.exists(filename):
        # The file doesn't exist so return. Nothing to send
        sys.stderr.write("File to send does not exist.\n")
        return

    f = open(filename, 'rb')
    segment = f.read(buff_size)
    while segment:
        sock.send(segment)
        segment = f.read(buff_size)
    f.close()

def get_cmd(filename, sock, buff_size):
    """ Takes filename and writes to it based on the read chunks from the open socket"""
    # Postpend downloaded files with name ".downloaded" since it's on NFS and should have the file on both computers
    f = open(filename + ".downloaded", 'wb')
    segment = sock.recv(buff_size)
    while segment:
        f.write(segment)
        segment = sock.recv(buff_size)
    f.close()
