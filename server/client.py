import argparse
import selectors
import socket
import os
import sys
import signal
from urllib.parse import urlparse

from socket import *
serverName = 'localhost'
serverPort = 1234

print("connecting to server...")


class client:
    def __init__(self, userName, address):
        self.userName = userName
        self.address = address
        parsedAddress = urlparse(address)
        self.host = parsedAddress.hostname
        self.port = parsedAddress.port


client1 = client("Terry", "chat://" + serverName + ":" + str(serverPort))

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print("connectiong succesful")
except:
    print("A connection error occured")


clientSocket.send(client1.userName.encode())


clientName = "Terry: "


sentence = clientName + input('Enter a message:\n')
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)
print('From Server:\n', modifiedSentence.decode())
modifiedSentence = clientSocket.recv(1024)
print('From Server:\n', modifiedSentence.decode())
modifiedSentence = clientSocket.recv(1024)
print('From Server:\n', modifiedSentence.decode())
# clientSocket.close()
