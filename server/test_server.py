import selectors
import socket
# from client.client import client1

sel = selectors.DefaultSelector()

userNames = []
connectorList = []
user = ""
stringMessage = ""
stringList = []


def accept(sock, mask):
    conn, addr = sock.accept()
    connectorList.append(conn)  # Should be ready
    print('Accepted connection from', addr)
    user = repr(conn.recv(1000))
    print('Waiting to recieve messages from user ' + user[1:])
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1000)
    if data:
        # print('echoing', repr(data), 'to', conn)
        stringMessage = repr(data)
        user, stringMessage = stringMessage.split(":", 1)
        user = user[2:]
        userNames.append(user)
        stringMessage = stringMessage.strip("'")
        print("message from: @" + user + "\n" + stringMessage)
        conn.send(data)
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
