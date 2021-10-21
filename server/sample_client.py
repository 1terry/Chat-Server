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
    selectors.EVENT_READ | selectors.EVENT_WRITE,
)

sock.sendall("Kohei".encode())
print("Server running, start messaging!")

while keep_running:
    # print('waiting for I/O')
    for key, mask in mysel.select(timeout=1):
        connection = key.fileobj
        client_address = connection.getpeername()
        # print('client({})'.format(client_address))

        if mask & selectors.EVENT_READ:
            # print('  ready to read')
            try:
                data = connection.recv(1024)
                if data:
                    print('  received {!r}'.format(data))
                    mysel.modify(sock, selectors.EVENT_WRITE)
            except:
                mysel.modify(sock, selectors.EVENT_WRITE)

            #how to change back and keep changing

        #YO WE DON"T NEED TO ECHO THE WRITE, ONLY READ

        if mask & selectors.EVENT_WRITE:
            # print('  ready to write\nEnter a message\n')
            # userInput = mysel.select([sys.stdin], [], [], 1)[0]
            input = select.select([sys.stdin], [], [], 1)[0]
            # userInput = input('')
            outgoing = input
            if input:
                value = sys.stdin.readline().rstrip()
                next_msg = ("Kohei: " + value).encode()
                sock.sendall(next_msg)    
                #Change this to signal
                if (value == "q"):
                    print ("Exiting")
                else:
                    print ("You entered: %s" % value)

            #try this
            try:
                data = connection.recv(1024)
                if data:
                    print('  received {!r}'.format(data))
            except:
                # print('waiting on data')
                doNothing = True

            # else:
            #     # Send the next message.
            #     # message = outgoing
            #     # print('')
            #     # next_msg = ("Terry: " + message).encode()
            #     try:
            #         data = connection.recv(1024)
            #         if data:
            #             print('  received {!r}'.format(data))
            #     except:
            #         print("waiting for message")
            #         mysel.modify(sock, selectors.EVENT_READ)
                # sock.sendall(next_msg)

print('shutting down')
mysel.unregister(connection)
connection.close()
mysel.close() 