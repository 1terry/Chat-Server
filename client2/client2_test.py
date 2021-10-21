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

sel = selectors.DefaultSelector()

class client:
    def __init__(self, userName, address):
        self.userName = userName
        self.address = address
        parsedAddress = urlparse(address)
        self.host = parsedAddress.hostname
        self.port = parsedAddress.port


client2 = client("Vanessa", "chat://" + serverName + ":" + str(serverPort))

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print("connectiong succesful")
except:
    print("A connection error occured, you may already be connected")


clientSocket.send(client2.userName.encode())


clientName = "Vanessa: "

exitCommand = False
while exitCommand == False:
    sentence = clientName + input('Enter a message:\n')
    #check that while enter is not pressed
    clientSocket.send(sentence.encode())

    # find a way to loop this
    modifiedSentence = clientSocket.recv(1024)
    if modifiedSentence != '':
        print(modifiedSentence)

# sentence = clientName + input('Enter a message:\n')
# clientSocket.send(sentence.encode())

# modifiedSentence = clientSocket.recv(1024)
# print('From Server:\n', modifiedSentence.decode())
# modifiedSentence = clientSocket.recv(1024)
# print('From Server:\n', modifiedSentence.decode())
# modifiedSentence = clientSocket.recv(1024)
# print('From Server:\n', modifiedSentence.decode())
# clientSocket.close()
