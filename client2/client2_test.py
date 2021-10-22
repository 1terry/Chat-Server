import selectors
import socket
import sys
import select
import signal
from urllib.parse import urlparse

mysel = selectors.DefaultSelector()
keep_running = True
# argument_count = (len(sys.argv))
inputArgs = sys.argv

#Isolates user name and host address from input
inputUser = inputArgs[1]
formattedAddress = inputArgs[2]

#Gets address from input and sets as 
parsedAddress = urlparse(formattedAddress) 
hostAddress = parsedAddress[1]
hostName, hostPort = hostAddress.split(":", 1)
hostPort = int(hostPort) 

#Registers socket with server using the parsed parameters
server_address = (hostName, hostPort)
print('connecting to {} port {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    sock.setblocking(False)
    print("Connection succesful, sending intro message...")
except:
    print("Server not found")
    doNothing = True
    sys.exit()

#Registers socket
mysel.register(
    sock, selectors.EVENT_WRITE
)

#Registers user
sock.send(("REGISTER " + inputUser + " CHAT/1.0").encode())
succesful = False

while keep_running:
    try:
        for key, mask in mysel.select(timeout=1):
            connection = key.fileobj

            input = select.select([sys.stdin], [], [], 1)[0]
            if input:
                value = sys.stdin.readline().rstrip()
                next_msg = (inputUser + ": " + value).encode()
                sock.sendall(next_msg)    

            data = repr(connection.recv(1024))
            data = data[2:len(data)-1]

            if data == "400 Invalid registration":
                print("Error, invalid registration")
                mysel.unregister(connection)
                connection.close()
                mysel.close() 
                sys.exit()

            #Checks for error codes and closes connection if error detected
            if data == "401 Client already registered":
                print("Error, client already registered")
                # next_msg = (inputUser + ": " + value).encode()
                mysel.unregister(connection)
                connection.close()
                mysel.close() 
                sys.exit()

            #Disconnects chat if server is closed and prints message
            if data == "DISCONNECT CHAT/1.0":
                print ("Sever closed, disconnecting user")
                connection.close()
                mysel.unregister(connection)
                mysel.close() 
                sys.exit()

            #try acceppting connection

            if data == "200 Registration successful":
                print("Server running, start messaging!")
                succesful = True
                # input = select.select([sys.stdin], [], [], 1)[0]
                # outgoing = input
                # if input:
                #     value = sys.stdin.readline().rstrip()
                #     next_msg = (inputUser + ": " + value).encode()
                #     print(next_msg)
                #     sock.sendall(next_msg)    
                  
            #Displays username and message recieved message only if sender is not the current user

            if succesful:
                try:
                    username, recievedMessage = data.split(":", 1)
                    if (username != inputUser):
                        print("    @" + username + ": " + recievedMessage)
                except:
                    doNothing = True


    #Catches socket error of recieving nothing, this just means no other clients have connected yet
    except (socket.error): 
        # print("Exception fuck")
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
    except Exception as e:
        print(e)
        sys.exit() 
