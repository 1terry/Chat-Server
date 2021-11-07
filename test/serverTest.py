
# import socket                   # Import socket module
# port = 60000                    # Reserve a port for your service.
# s = socket.socket()             # Create a socket object
# host = socket.gethostname()     # Get local machine name
# s.bind((host, port))            # Bind to the port
# s.listen(5)                     # Now wait for client connection.

# print('Server listening....')

# while True:
#     conn, addr = s.accept()     # Establish connection with client.
#     print('Got connection from ' + str(addr))
#     data = conn.recv(1024)
#     print('Server received' + repr(data))

#     filename = 'test.txt'
#     f = open(filename, 'rb')
#     l = f.read(1024)
#     while (l):
#         conn.send(l)
#         print('Sent ', repr(l))
#         l = f.read(1024)
#     f.close()

#     print('Done sending')
#     conn.send(('Thank you for connecting').encode())
#     conn.close()
#     break

file1 = open("myfile.txt", "w")
file1.write("This is Delhi \nThis is Paris \nThis is London \n")
file1.close()

# useful stuff

# if ("fileStart" in stringMessage):
#                 parts = stringMessage.split(": ")
#                 fileName = parts[2]

#                 # Gets the location of the current directory
#                 while (stringMessage != "fileEnd"):
#                     # recieves file
#                     with open(fileName, 'w') as f:
#                         print("file recieved from: " + userNames[elementPosition])
#                         while True:
#                             print('receiving data...')
#                             data = conn.recv(1000)
#                             print('data:', (data))
#                             if not data:
#                                 break
#                         # write data to a file
#                         f.write(data)
