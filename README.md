# Chat-Server
Instructions to run:

First, open a terminal in linux.

Then, navigate to the folder containing the files server.py and client.py.

run server.py using the following command:
- python3 server.py

If using python3 does not work, try using python instead.

The server is now open and ready to recieve input from the client

To run the client, use the following command:

- python3 client.py username chat://host:port

host will likely be localhost, and the port will be specified after running the server.
You can run as many clients as you want by opening new terminals as long as they have different usernames, or you will
encounter an error from the server.

An example of running the server and several clients are below.

Server: 
-python3 server.py

Client:

-python3 client.py first_user chat://localhost:34749
-python3 client.py second_user chat://localhost:34749

You will then be able to type messages in the client, which will output results in both the other client and the server.