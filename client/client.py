"""
File for chat client
Created for CS 3357 By Terrence Ju
Oct 21, 2021
Client will take in parameters as arguments in the terminal and connect to the server
Client will be able to connect to other clients and send and recieve messages from them
"""

#https://www.youtube.com/watch?v=7Z_uQKV7RLI

# Libraries and packages used
import selectors
import socket
import sys
import select
import signal
import os

from urllib.parse import urlparse

# Initializes variables
mysel = selectors.DefaultSelector()
keep_running = True
inputArgs = sys.argv
global hostPort
# Method checkData takes in server data as param and checks the control messages and outputs results


def checkData(data):

    # Responds to 400 message by shutting everything down and printing error
    if data == "400 Invalid registration":
        print("Error, invalid registration message")
        mysel.unregister(connection)
        connection.close()
        mysel.close()
        sys.exit()

    # Responds to 401 message by shutting everything down and printing error
    if data == "401 Client already registered":
        print("Error, client already registered")
        mysel.unregister(connection)
        connection.close()
        mysel.close()
        sys.exit()

    # Disconnects chat if server is closed and prints message
    if data == "DISCONNECT CHAT/1.0":
        print("Disconnecting user...")
        connection.close()
        mysel.unregister(connection)
        mysel.close()
        print("User disconnected")
        sys.exit()

    # If data is a file being sent
    if data == "File-Sent":
        print("file being recived")

    # Prints message if connection is accepted succesfully
    if data == "200 Registration successful":
        print("Server running, start messaging!")


# Tries connecting to server using formatted input from user
try:
    # Exits on wrong format
    if (len(inputArgs) > 3):
        print("Too many arguments")
        sys.exit()

    # Parses user name and server address from parameters and stores as variables
    inputUser = inputArgs[1]
    formattedAddress = inputArgs[2]
    parsedAddress = urlparse(formattedAddress)
    hostAddress = parsedAddress[1]
    hostName, hostPort = hostAddress.split(":", 1)
    hostPort = int(hostPort)

    # Registers socket with server using the parsed parameters, tries connecting to server and sets blocking to flase
    server_address = (hostName, hostPort)
    print('connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.setblocking(False)
    print("Connection succesful, sending intro message...")

# Client closes on bad input
except:
    print("Server not found, check your commands and run again")
    doNothing = True
    sys.exit()

# Registers socket and sends registration message
mysel.register(sock, selectors.EVENT_WRITE)
sock.send(("REGISTER " + inputUser + " CHAT/1.0").encode())

# Infinite loop to recieve input from server
while keep_running:
    try:
        # Loops and checks for server input
        for key, mask in mysel.select(timeout=1):
            connection = key.fileobj

            # Checks user input in terminal and sends to
            input = select.select([sys.stdin], [], [], 1)[0]
            if input:
                # working
                value = sys.stdin.readline().rstrip()

                # If command !attach is used, tries to send file
                if "!attach" in value:
                    # This stuff works so far
                    next_msg = (inputUser + ": " + value).encode()
                    sock.sendall(next_msg)
                    parts = value.split()
                    fileName = parts[1]
                    givenTerms = parts[2]

                    #File size 
                    print("File size: ", os.path.getsize(os.path.basename(fileName)))

                    print("Sending: " + fileName)
                   
                    #Sending code in here
                    BUFFER_SIZE = 4096
                        # send the filename and filesize

                        # start sending the file
                    # sock.sendall("!READING".encode())
                    with open(fileName, "rb") as f:
                        while True:
                            # read the bytes from the file
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                # file transmitting is done
                                break
                            #DO i have to encode this?
                            message = "!READING".encode() + bytes_read
                            sock.sendall(message)
                            print("Sending ..." + repr(message))
                    print("File sent")
                    #END OF COPIED PART
                    
                   

                # If !attach is not entered
                else:
                    next_msg = (inputUser + ": " + value).encode()
                    sock.sendall(next_msg)
                    print("SENT" + value)

            # Recieves and formats data from server
            data = repr(connection.recv(1024))
            data = data[2:len(data)-1]

            # Checks various control messages
            checkData(data)

            # Filters server messages so that only messages from other users are displayed
            try:
                username, recievedMessage = data.split(":", 1)
                if (username == "Users" or username == "Followed items" or username == "Now following" or
                username == "Error"):
                    print(username + ": " + recievedMessage)
                elif (username != inputUser):
                    print("   @" + username + ": " + recievedMessage)

            # Catches a differently formatted message and ignores
            except:
                doNothing = True

    # Catches socket error of recieving nothing, this just means no other clients have connected yet
    except (socket.error):
        doNothing = True
        pass

    # Catches control-c, prints shutdown message and disconnects and unregisters user
    except KeyboardInterrupt:
        print("\n Interrupt Recieved, disconnecting user")
        sock.send("DISCONNECT username CHAT/1.0".encode())
        mysel.unregister(connection)
        connection.close()
        mysel.close()
        sys.exit()
        pass

    # Server is likely closed, so we exit the program
    except Exception:
        sys.exit()

