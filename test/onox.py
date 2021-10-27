frame):
    print('Interrupt received, shutting down ...')
    sys.exit(0)


# Our main function.

def main():
    # Register our signal handler for shutting down.

    signal.signal(signal.SIGINT, signal_handler)

    # Create the socket.  We will ask this to work on any interface and to pick
    # a free port at random.  We'll print this out for clients to use.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 0))
    print('Will wait for client connections at port ' + str(server_socket.getsockname()[1]))
    print('Waiting for incoming client message ...')

    #client_socket , address= server_socket.accept() 

    
    
    ###################################################

    introMessageString="Accepted connection from client address: "
    introMessage = introMessageString.rstrip().encode()
    listOfAddresses=[]
    ####################################################
    
    # Keep the server running forever.
    #Accepting message from the client
    while (1):

        userID, addr = server_socket.recvfrom(BUFFER_SIZE)
        message, addr = server_socket.recvfrom(BUFFER_SIZE)

        


        if message.decode('utf8', 'strict') == introMessage.decode('utf8', 'strict'):
            print(message.decode(),addr)
            print("Connection to client established, waiting to receive messages from user '",userID.decode(),",...")
            #Creating a list of addresses
        
            if addr not in listOfAddresses:
                listOfAddresses.append(addr)
            
            
        else:
            #What server prints
            print("Received message from ",userID.decode()," :",message.decode())
            #print("Received message from ",userID.decode()," :",message.decode(),"test: ",addr)
            #print(listOfAddresses)
            #What all other clients except for the current client prints
            for address in listOfAddresses:
                if address!=addr:
                    server_socket.sendto(bytes("@"+userID.decode()+": "+message.decode(),"utf-8"),address)

            
        #print(message.decode(), addr) if message.decode()== introMessage.decode() else print('Received message from user :', message.decode())
        
        #Condtion when a client closes, then pop from the list

       
        

if _name_ == '_main_':
    main()