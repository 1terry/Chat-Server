"""
File for chat server
Created for CS 3357 By Terrence Ju
Oct 21, 2021
Server will accept connections from clients and return messages to all clients
Server will close client connections when it closes
Server will also display control messages such as error and disconnect messages
"""

#Libraries used
import selectors
import socket
import sys

#Initializes selectors and variables
sel = selectors.DefaultSelector()
userNames = []
connectorList = []
user = ""
stringMessage = ""
stringList = []
initField = []

#Method runs on acceptance of a new connection, takes in input of socket and mask
def accept(sock, mask):

    #Tries accepting registered user
    try:
        #Accepts connection from socket and formats result
        connection, address = sock.accept()
        user = repr(connection.recv(1000))
        connectorList.append(connection)
        initField = user.split()
        user = initField[1]

        #Checks length of the registration message to make sure it's formatted properly
        if (len(initField) != 3):
            connectorList.remove(connection)
            raise Exception

        print('Accepted connection from', address)

        #Displays error if client is already registered and closes connection
        if (user in userNames):
            connection.sendall(("401 Client already registered").encode())
            print("Client already registered, closing connection")
            connectorList.remove(connection)

        #Otherwise, registers connection and user name and sends message to client
        else:
            userNames.append(user)
            print('Connection established, waiting to recieve messages from user "' + user + '"...')
            connection.setblocking(False)
            sel.register(connection, selectors.EVENT_READ, read)
            connection.sendall(("200 Registration successful").encode())

    #Returns error if registration message is bad
    #This shouold never happen however, as the registration fromat will be hardcoded
    except:
        print("Error, invalid registration")
        connection.sendall(("400 Invalid registration").encode())
    

#Method defines read state of the server, takes in a connection and a mask
def read(conn, mask):
    data = conn.recv(1000)
    if data:
        #Formats message recieved
        stringMessage = repr(data)
        stringMessage = stringMessage[2:len(stringMessage)-1]

        #Disconnects user if disconnect is sent, removes and unregisters connections and prints result
        if stringMessage == "DISCONNECT username CHAT/1.0":
            elementPosition = connectorList.index(conn)
            elementName = userNames[elementPosition]
            print("Recieved message from user " + elementName + ": " + "DISCONNECT " + elementName + " CHAT/1.0")
            print('Disconnecting user ' + elementName)
            userNames.remove(elementName)
            sel.unregister(conn)
            connectorList.remove(conn)
            conn.close()

        #Formats message from user and prints
        else:
            user, stringMessage = stringMessage.split(":", 1)
            formattedMessage = "Recieved message from user " + user + ": " + stringMessage
            print(formattedMessage)

            #Sends message to all connections
            for x in connectorList:
                x.send((user + ": " + stringMessage).encode())


#Binds socket and generates a random port, then listens on it
sock = socket.socket()
sock.bind(('localhost', 0)) 
port = str(sock.getsockname()[1])
sock.listen(100)

#Prints message displaying port and registers socket with selector
print('The server will wait for connections at port: ' + port)
print('The server is ready to recieve messages')
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

#Loop checking for input 
while True:
    #Loops read and write to respond to events
    try:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    #On control + c, system exits and sends message to all connected clients, and closes server
    except KeyboardInterrupt:
        print ("\n Interrupt recieved, server shutting down")
        for x in connectorList:
            x.send(("DISCONNECT CHAT/1.0").encode())
        sel.close() 
        sys.exit()