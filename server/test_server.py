import selectors
import socket
# from client.client import client1

# super good
# https://realpython.com/python-sockets/#multi-connection-client-and-server

sel = selectors.DefaultSelector()

#Initializing Variables
userNames = []
connectorList = []
user = ""
stringMessage = ""
stringList = []
initField = []

#Defines acceptance of a new connection
def accept(sock, mask):
    try:
        connection, address = sock.accept()
        connectorList.append(connection)
        print('Accepted connection from', address)
    except:
        print("Error, invalid registration")

    #format text
    user = repr(connection.recv(1000))
    initField = user.split()
    user = initField[1]
    if (userNames.__contains__(user)):
        connection.send("401 Client already registered".encode())
    else:
        userNames.append(user)
    #Check if user is registered

    print('Waiting to recieve messages from user ' + user)
    connection.setblocking(False)
    sel.register(connection, selectors.EVENT_READ, read)

#Defines read state of server
def read(conn, mask):
    data = conn.recv(1000)
    if data:
        stringMessage = repr(data)
        user, stringMessage = stringMessage.split(":", 1)
        user = user[2:]
        userNames.append(user)
        stringMessage = stringMessage.strip("'")
        formattedMessage = "Recieved message from user " + user + ": " + stringMessage
        print(formattedMessage)
        # make a for loop here for each connector
        for x in connectorList:
            x.send((user + ": " + stringMessage).encode())

    else:
        print('closing', conn)
        sel.unregister(conn)
        connectorList.remove(conn)
        conn.close()


sock = socket.socket()
sock.bind(('localhost', 1234)) 
sock.listen(100)
print('The server is ready to recieve messages')
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
