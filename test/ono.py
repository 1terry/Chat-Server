#Client Server
import socket
import argparse
import sys
import select
from urllib.parse import urlparse
import selectors
# Define a constant for our buffer size

BUFFER_SIZE = 2048

# Our main function.

def main():

    # Check command line arguments to retrieve a URL.

    parser = argparse.ArgumentParser()
    ###################################
    parser.add_argument("userID", type=str, help=" User ID of the user")
    ###################################
    #parser.add_argument("host", help="Host name of server")    
    #parser.add_argument("port", help="Port number of server")
    parser.add_argument("hostAndport", help="Host and Port number of server")
    
    args = parser.parse_args()
    #host = args.host
    #port = int(args.port)
    hostAndport=args.hostAndport
    o = urlparse(str(hostAndport))
    host=o.hostname
    port=int(o.port)
    userID = args.userID
    #print(userID)
    
    
    # Now we try to make a connection to the server.
    print('Connecting to server')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Connection to server established. Sending intro message...")
    
    #Test to send intro message to server
    ###############################################################
    
    introMessage = "Accepted connection from client address: "
    client_socket.sendto(userID.rstrip().encode(), (host,port))
    client_socket.sendto(introMessage.rstrip().encode(), (host,port))
    
    ###############################################################
    #Confrims that connection has been established
    print("")
    print("Registration successful. Ready for messenging!")

    
    ##############################################
    
    selector = selectors.DefaultSelector()

    # register the client socket and set it to read
    selector.register(client_socket, selectors.EVENT_READ)

    # register the stdin object and set it to write
    selector.register(sys.stdin, selectors.EVENT_READ)

    while True:
        for key, mask in selector.select():
            # rest of your loop
            input = select.select([sys.stdin], [], [], 1)[0]
            if input:
                value = sys.stdin.readline().rstrip()
        
                if (value == "q"):
                    print("Exiting")
                    sys.exit(0)
                else:
                    #print("You entered: %s" % value)
                    
                    client_socket.sendto(userID.rstrip().encode(), (host,port))
                    client_socket.sendto(value.encode(), (host,port))

                    #Receiving message back from server
                    msg = client_socket.recv(2048)
                    if msg:
                        print(msg.decode())
            else:
                continue


if _name_ == '_main_':
    main()