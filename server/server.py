import selectors
import socket
import sys

sel = selectors.DefaultSelector()

#Initializing Variables
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
        connection, address = sock.accept()
        user = repr(connection.recv(1000))
        connectorList.append(connection)
        initField = user.split()
        user = initField[1]
        print('Accepted connection from', address)

        if (user in userNames):
            connection.sendall(("401 Client already registered").encode())
            print("Client already registered, closing connection")
            connectorList.remove(connection)
        else:
            userNames.append(user)
            print('Waiting to recieve messages from user ' + user)
            connection.setblocking(False)
            sel.register(connection, selectors.EVENT_READ, read)
            # connection.sendall(("200 Registration successful").encode())

    #Returns invalid registration code if there is an error
    except:
        print("Error, invalid registration")
        connection.sendall(("400 Invalid registration").encode())
    

#Defines read state of server
def read(conn, mask):
    data = conn.recv(1000)
    if data:
        #Formats message
        stringMessage = repr(data)
        stringMessage = stringMessage[2:len(stringMessage)-1]
        #Disconnects user if message is sent
        if stringMessage == "DISCONNECT username CHAT/1.0":
            elementPosition = connectorList.index(conn)
            elementName = userNames[elementPosition]
            print('Disconnecting user ' + elementName)
            userNames.remove(elementName)
            sel.unregister(conn)
            connectorList.remove(conn)
            conn.close()

        else:
            user, stringMessage = stringMessage.split(":", 1)
            formattedMessage = "Recieved message from user " + user + ": " + stringMessage
            print(formattedMessage)

            # sends message to all connections
            for x in connectorList:
                x.send((user + ": " + stringMessage).encode())



sock = socket.socket()
sock.bind(('localhost', 0)) 
port = str(sock.getsockname()[1])
sock.listen(100)
print('The server is ready to recieve messages')
print('The server will wait for connections at port: ' + port)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

#Loop checking for input from connection
while True:
    try:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    #On control + c, system exits and sends message to all connected clients
    except KeyboardInterrupt:
        print ("\n Interrupt recieved, server shutting down")
        for x in connectorList:
            x.send(("DISCONNECT CHAT/1.0").encode())
        sel.close() 
        sys.exit()
