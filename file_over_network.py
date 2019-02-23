import sys
from socket import *

def put_cmd(filename, sock, buff_size):
    """ Takes filename and uploads by reading chunks and sending them over the open socket"""
    f = open(filename, 'rb')
    segment = f.read(buff_size)
    while segment:
        sock.send(segment)
        segment = f.read(buff_size)
    f.close()

def get_cmd(filename, sock, buff_size):
    """ Takes filename and writes to it based on the read chunks from the open socket"""
    f = open("downloaded_" + filename, 'wb')
    segment = sock.recv(buff_size)
    while segment:
        f.write(segment)
        segment = sock.recv(buff_size)
    f.close()
