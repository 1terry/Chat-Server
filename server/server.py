import argparse
import selectors
import socket
import os
import sys
import signal
from urllib.parse import urlparse

from socket import *
# randomize number later
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capsSentence = sentence.upper()
    connectionSocket.send(capsSentence.encode())
    connectionSocket.close()



# useful documentation

# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse
