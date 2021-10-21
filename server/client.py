import selectors
import socket
import sys
import select

mysel = selectors.DefaultSelector()
keep_running = True

# Connecting is a blocking operation, so call setblocking()
server_address = ('localhost', 1234)
print('connecting to {} port {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False)

mysel.register(
    sock, 
    selectors.EVENT_WRITE,
)

#Registers user
inputUser = "Terry"
sock.sendall(("REGISTER " + inputUser + " CHAT/1.0").encode())

#Checks if data is being sent from server, in case there is an error with registration 
try:
    #returning server thingy
    data = repr(connection.recv(1024))
    if data == "401 Client already registered":
        print("Error, client already registered")
    elif data == "400 Invalid registration":
        print("Error, invalid registration")
    sys.exit(0)
    doNothing = True
except:
    #
    doNothing = True

print("Server running, start messaging!")

while keep_running:
    # print('waiting for I/O')
    for key, mask in mysel.select(timeout=1):
        connection = key.fileobj

        if mask & selectors.EVENT_WRITE:
            input = select.select([sys.stdin], [], [], 1)[0]
            outgoing = input
            if input:
                value = sys.stdin.readline().rstrip()
                next_msg = (inputUser + ": " + value).encode()
                sock.sendall(next_msg)    
                #Change this to signal
                # if (value == "q"):
                #     print ("Exiting")
                # else:
                    # print ("You entered: %s" % value)
                    # doNothing = True

            #try this
            try:
                data = repr(connection.recv(1024))
                data = data.strip("'")
                username, recievedMessage = data.split(":", 1)
                username = username[2:]
                if (username != inputUser):
                    print("    @" + username + ": " + recievedMessage)
            except:
                # does nothing
                doNothing = True

print('shutting down')
mysel.unregister(connection)
connection.close()
mysel.close() 
