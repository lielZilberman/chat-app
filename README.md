# simple-chat-app

a final project in communication course Ariel University

*IMPORTANT NOTE : THIS CHAT RUNS LOCALLY ONLY.
David Ehevich -212757405
Liel Zilberman - 212480974

__Running the project :__

Via CMD:

go to the directory in which you installed the project and open via CMD, to open the server you must type in server.py which will run the server which the chat works on.
To open a client open seperate CMD and type in client.py , this will open the GUI in which you can login and interate with the chat. Each CMD running client.py is a different user(client).

Via IDE:

Same as through the CMD just open the terminal in the IDE and type the same command lines you would type in CMD.

Explaining part 1:

This chat works and communicates via TCP communication protocol.

How we kept our USER CONNECTIONS:

To keep the clients connections connected to their user name we used a dictionary data structure, the fromat is : {clientUserName:connectionScoketObject}

How to store files on the server:

To store the files on the server you have to download or create manually the ServerFiles folder and it has to be in the same directory as the client.py and server.py

Server side:

Since we have been requested to create a multi chat room , we needed to use threads since socket.recv() and socket.accept() are blocking commands meaning other lines will not be 
executed until they are complete, so one thread will wait for new connections and on thread will wait for data for the client , each client has his own thread since the server receives 
data from each client there for each client needs a recv command.

Client side:

Features of the chat in this part (And explaining how every feature works behind the scenes):

 Disconnecting : 
 
 You have 2 ways to logout , pressing x on the gui screen or pressing the logout button , how this works , when the users makes one of this actions a string is sent to the 
 server , the server is always waiting for data for each client  , when the server receives the "DISCONNECT" string after the client disconnectes, the server closes the connection between the user and the server and removes the connection socket from the data structure(dictionary) in which we kept the users data.
 
 Show server Files:
 
 When the button show files is pressed we sent a string "%SHOW_SERVER_FILES%" to the server so the server sends all of the available files on the server to the client, with a string, "SERVER_FILES~(string of the server files)" the client receives this message and it sees it's server files so it pops a window listing all of the files.
 
 Clear chat:
 
 Clear the chat on the chat window , server is not involved.
 
 Show online:
 
 When the button is pressed the we send "%SHOW_ONLINE%" string so the server sends back a string: "ONLINE_USERS+(name of all the online users)", all of the client's user names are taken from the dictionary data structure. 
 
 Download files from the server:
 
 The client enters the name of the file which he wants to download from the server , and in what name he wantes to keep it on his computer.
 When the Download button is pressed the server receives a "%DOWNLOAD_FILE%" string , so he open the file in readmode , and since we send a certain amout of bytes each send() command we run a loop to send all of the bytes of the file. On the client side we receive "DOWNLOAD_FILE" so we know the server got the name of the file , and then we send a "ACK" from the user to let the server know he can start sending the bytes of the file, after sending the "ACK" the user is waiting for data , and when the server receives the "ACK" , only then he starts sending. If the file does not exist in the server a "File does not exist message will appear to the user"
 
 Message types:
 
 PUBLIC:
 The client is able to send public messages , he just has to leave the "send to" square blank, when the send button is pressed the server receives the message and then sends all the user connected the message.
 
 PRIVATE:
 The client can send private messages by typing the name of the username in the "send to" square , if the the user does not exist the server will notify the client.
 We check on the client side if the send to is not empty , if not then we add the name of the user name to the string , and then server sends the message only to the specified   username.
 
 Taken User Name: 
 
 Part 2:

All of this part features still work via TCP protocol except Downloading the file downloading the files is via UDP protocol.
All of the code in both parts is identical except the donwload file function.

When downloading a file we use the same method with ACK to the server and only then he starts sending data , since we created a seperate socket using UDP protocol , when a download is requested we create a seperate socket and therefore we need another thread , so we create a new thread for downloading a file with UDP, the thread of the TCP socket waites to receive the download has been finished(only when it's finished) while the UDP thread download the file.


