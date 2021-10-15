import argparse
import selectors
import socket
import os
import sys
import signal
from urllib.parse import urlparse

from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientName = '\nBob: '

sentence = clientName + input('Type message:') 
clientSocket.send(sentence.encode())


modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()




