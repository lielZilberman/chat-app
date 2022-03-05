# simple-chat-app

a final project in communication course Ariel University

*IMPORTANT NOTE : THIS CHAT RUNS LOCALLY ONLY.

__Running the project :__

VIA CMD:

go to the directory in which you installed the project and open via CMD, to open the server you must type in server.py which will run the server which the chat works on.
To open a client open seperate CMD and type in client.py , this will open the GUI in which you can login and interate with the chat. Each CMD running client.py is a different user(client).

VID IDE:

Same as through the CMD just open the terminal in the IDE and type the same command lines you would type in CMD.

Explaining part 1:

This chat works and communicates via TCP communication protocol.

How we kept our USER CONNECTIONS:

Server side:

Since we have been requested to create a multi chat room , we needed to use threads since socket.recv() and socket.accept() are blocking commands meaning other lines will not be 
executed until they are complete, so one thread will wait for new connections and on thread will wait for data for the client , each client has his own thread since the server receives 
data from each client there for each client needs a recv command.

Client side:

Features of the chat in this part (And explaining how every feature works behind the scenes):

 Disconnecting : 
 
 You have 2 ways to logout , pressing x on the gui screen or pressing the logout button , how this works , when the users makes one of this actions a string is sent to the 
 server , the server is always waiting for data for each client  , when the server receives the "DISCONNECT" string after the client disconnectes, the server closes the connection between the 
 user and the server


