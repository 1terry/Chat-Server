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
import os
from array import *

#Initializes selectors and variables
sel = selectors.DefaultSelector()
userNames = []
connectorList = []
user = ""
stringMessage = ""
stringList = []
initField = []
followList = []

def checkCommands(userCommand, user_index, user):
    #All strings have a space at the start when sent, so we include these in comparisons
    userList = ""
    followedTerms = ""
    buffer_size = 0

    #Checks if list command is entered and sends using :, as this will be split
    if (userCommand == " !list"):
        for x in userNames:
           userList = userList + x + ", "
        print("Users: " + userList)
        connectorList[user_index].send(("Users: " + userList).encode())

    #If the user enters !follow?, list will be displayed
    elif (userCommand == " !follow?"):
            #Gets list and prints as string
        for x in followList[user_index]:
            followedTerms = followedTerms + x + ", "
            displayFollowed = "Followed items: " + followedTerms
        print(displayFollowed)
        connectorList[user_index].send((displayFollowed).encode())

    #Check that follow is 

    #Adds item to follow list
    elif ("!follow" in userCommand):

            #Gets list and prints as string
        for x in followList[user_index]:
            followedTerms = followedTerms + x + ", "
            displayFollowed = "Followed items: " + followedTerms

        topics = userCommand.split()

        if topics[1] in followList[user_index]:
           print("Topic already present")
           connectorList[user_index].send(("Error: Topic already present").encode()) 

        followList[user_index].append(topics[1])
        print(displayFollowed)

    #removes item from follow list
    elif ("!unfollow" in userCommand):

        for x in followList[user_index]:
            followedTerms = followedTerms + x + ", "
            displayFollowed = "Followed items: " + followedTerms
        print(displayFollowed)

        topics = userCommand.split()

        if (topics[1] == "@all" or topics[1] == userNames[user_index]):
            connectorList[user_index].send(("Error: Cannot remove tags").encode())
            print("Cannot remove tags")

        #Tries to remove the followed item from the list and outputs error if it does not exist
        else:
            try:
                followList[user_index].remove(topics[1])
            except:
                connectorList[user_index].send(("Error: Tags not in follow list").encode())
                print("Tags not in follow list")

        print(displayFollowed)

    
    #If the user enters exit, the server exits
    #Make sure to deal with connections and stuff
    elif ("!exit" in userCommand):
        connectorList[user_index].send(("DISCONNECT CHAT/1.0").encode()) #Remove from lists and such
      
    #Attaching a file
    elif ("!attach" in userCommand):
        parts = userCommand.split()
        fileName = parts[1]
        givenTerms = parts[2]

        #Gets the location of the current directory
        print(os.path.basename(fileName))

        #Gets the size of the file, enters an error if the file is not found
        try:
            size = os.path.getsize(os.path.basename(fileName))
            print("File is " + str(size) + " bytes")
            buffer_size = int(size)

            # Not super sure how to get this working
            # with open(fileName, "wb") as f:
            #     while True:
            #         bytes_read = client_socket.recv(buffer_size)
            #         if not bytes_read:
            #             break
            #         f.write(bytes_read)
            #     print("file writing done")
            # Everything outside this section works tho

        except:
            print("File not found, please check file name")

    #Otherwise, broadcasts the message to other users
    else:    

        #loop through each word to compare followed terms to the users message
        userCommand = userCommand.split()
        userMessage = ""
        
        for x in userCommand:
            userMessage = userMessage + " " + x
            print(x)

        #Consider making seperate loops instead of nested loops?

        for x in userCommand:

            #Change these shitty variable names
            for y in followList:
                for z in y:
                    #Breaks out of loop of current user
                    if x == z:
                        print(user + ": " + userMessage)
                        connectorList[followList.index(y)].send((user + ": " + userMessage).encode())
                        break
            


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

        #Ensures that user cannot register as "all"
        elif (user == "all"):
            connection.sendall(("401 Client already registered").encode())
            print("Cannot register under reserved username, closing connection")
            connectorList.remove(connection)

        #Otherwise, registers connection and user name and sends message to client
        else:
            userNames.append(user)
            newUser = len(userNames) - 1
            followList.append([])     #Increases list size and adds items
            followList[newUser].append("@" + user)
            followList[newUser].append("@all")
            print('Connection established, waiting to recieve messages from user "' + user + '"...')
            connection.setblocking(False)
            sel.register(connection, selectors.EVENT_READ, read)
            connection.sendall(("200 Registration successful").encode())

    #Returns error if registration message is bad
    #This shouold never happen however, as the registration fromat will be hardcoded
    except Exception as e:
        print("Error, invalid registration")
        connection.sendall(("400 Invalid registration").encode())
        print(e)
    

#Method defines read state of the server, takes in a connection and a mask
def read(conn, mask):
    data = conn.recv(1000)
    if data:
        #Formats message recieved
        stringMessage = repr(data)
        stringMessage = stringMessage[2:len(stringMessage)-1]
        elementPosition = connectorList.index(conn)


        #Disconnects user if disconnect is sent, removes and unregisters connections and prints result
        if stringMessage == "DISCONNECT username CHAT/1.0":
            # elementPosition = connectorList.index(conn)
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


            checkCommands(stringMessage, elementPosition, user)

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
