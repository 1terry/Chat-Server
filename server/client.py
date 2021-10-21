import selectors
import socket
import sys
import select
import signal

mysel = selectors.DefaultSelector()
keep_running = True
# argument_count = (len(sys.argv))
inputArgs = sys.argv

#Find Finds secont
formattedAddress = inputArgs[2]
print(formattedAddress)



# if data == "400 Invalid registration":
#     mysel.unregister(connection)
#     connection.close()
#     mysel.close() 
#     print("Error, invalid registration")
#     exit()

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
inputUser = "terry"
sock.sendall(("REGISTER " + inputUser + " CHAT/1.0").encode())

print("Server running, start messaging!")

while keep_running:
    # print('waiting for I/O')
    try:
        for key, mask in mysel.select(timeout=1):
            connection = key.fileobj

        # try:
        # if mask & selectors.EVENT_WRITE:
            input = select.select([sys.stdin], [], [], 1)[0]
            outgoing = input
            if input:
                value = sys.stdin.readline().rstrip()
                next_msg = (inputUser + ": " + value).encode()
                sock.sendall(next_msg)    

            #try acceppting connection
            # try:
            data = repr(connection.recv(1024))
            data = data[2:len(data)-1]

            #Checks for error codes and closes connection if error detected
            if data == "401 Client already registered":
                print("Error, client already registered")
                # next_msg = (inputUser + ": " + value).encode()
                mysel.unregister(connection)
                connection.close()
                mysel.close() 
                sys.exit()

            #Disconnects chat if server is closed and prints message
            elif data == "DISCONNECT CHAT/1.0":
                print ("Sever closed, disconnecting user")
                connection.close()
                mysel.unregister(connection)
                mysel.close() 

            #Make sure to count : when using string
            username, recievedMessage = data.split(":", 1)
            # username = username[2:]
            if (username != inputUser):
                print("    @" + username + ": " + recievedMessage)

            
    except (socket.error): 
        # print(e)
        # does nothing
        doNothing = True
        pass
            
    #Catches control-c, prints shutdown message and disconnects user from server
    except KeyboardInterrupt:
        print ("\n Interrupt Recieved, disconnecting user")
        sock.send("DISCONNECT username CHAT/1.0".encode())
        mysel.unregister(connection)
        connection.close()
        mysel.close() 
        sys.exit()
        pass 

    #Server is likely closed or another error has been encountered so we exit the program
    except:
        sys.exit() 

