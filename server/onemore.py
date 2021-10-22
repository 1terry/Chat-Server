import selectors
import socket
# from client.client import client1

# super good
# https://realpython.com/python-sockets/#multi-connection-client-and-server

sel = selectors.DefaultSelector()

userNames = []
connectorList = []
user = ""
stringMessage = ""
stringList = []


def accept(sock, mask):
    try:
        connection, address = sock.accept()
        connectorList.append(connection)
        print('Accepted connection from', address)
    except:
        if (connectorList.__contains__(connection)):
            print("Error: Already connected")

    user = repr(connection.recv(1000))
    print('Waiting to recieve messages from user ' + user[1:])
    connection.setblocking(False)
    sel.register(connection, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1000)
    if data:
        stringMessage = repr(data)
        user, stringMessage = stringMessage.split(":", 1)
        user = user[2:]
        userNames.append(user)
        stringMessage = stringMessage.strip("'")
        formattedMessage = "message from: @" + user + "\n" + stringMessage
        print(formattedMessage)
        # make a for loop here for each connector
        for x in connectorList:
            x.send(formattedMessage.encode())

    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen(100)
print('The server is ready to recieve messages')
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

# Signal handler for graceful exiting.


def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')


while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)