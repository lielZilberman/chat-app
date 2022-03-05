import threading
import socket
import sys
import os

#########################################################################
# IMPORTANT:

# All of the explanation about the server side commands are in the read me in our github repo

#########################################################################
format = "utf-8"
Users = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddr = socket.gethostbyname(socket.gethostname())
serverPort = 50000
server.bind((serverAddr, serverPort))


def newUser(connection, addr):
    denied = True
    userName = ""
    while denied:
        try:
            check = False
            message = connection.recv(2048).decode()
            connection.send("ACK-RECEIVED".encode())
            userName = connection.recv(2048).decode()
            for i in Users:
                if userName == i:
                    connection.send(("%USERNAME_DENIED%").encode())
                    check = True
            if check:
                continue
            connection.send("APPROVED".encode())
            denied = False
        except:
            continue
    for i in Users:
        Users[i].send(("" + userName + " Has CONNECTED to the chat!\n").encode())
    Users[userName] = connection
    connection.send(("You have been CONNECTED to the chat!\n").encode())
    while True:
        try:
            message = connection.recv(2048).decode()
            mone = 0
            for i in message:
                mone += 1
            if message == "%SHOW_SERVER_FILES%":
                send_data = ""
                files = os.listdir("ServerFiles")
                if len(files) == 0:
                    connection.send("%SHOW_SERVER_FILES%~Server has no FILES".encode())
                else:
                    send_data += "\n".join(f for f in files)
                    connection.send(("%SHOW_SERVER_FILES%~" + send_data).encode())
            elif message[0:13] == "DOWNLOAD_FILE":
                fileList = message.split("~")
                try:
                    file = open("ServerFiles/" + fileList[1], "rb")
                except:
                    connection.send("FILE NOT FOUND".encode())
                    continue
                connection.send(("DOWNLOAD_FILE~" + fileList[2]).encode())
                ackApp = connection.recv(2048).decode()
                try:
                    if ackApp == "%GOT-ACK%":
                        data = file.read(2048)
                        while data:
                            connection.send(data)
                            data = file.read(2048)
                        connection.send(b"%IMAGE_COMPLETED%")
                        file.close()
                except:
                    connection.send("Failed to download file\n".encode())
                    continue
            elif message[0:14] == "disconnectUser":
                connection.close()  # Closing client's socket
                discList = message.split("~")
                Users.pop(discList[1])  # Removing from the dictionary
                for i in Users:
                    Users[i].send(("" + userName + " Has DISCONNECTED from the chat!\n").encode())
                sys.exit()  # Closing thread
            elif message == "showUsersOnline":
                usersOnline = "showUsersOnline"
                for i in Users:
                    usersOnline = usersOnline + "~" + i
                connection.send(usersOnline.encode())
            elif message[0:6] == "prvMsg":
                prvUser = message[6:]
                mone = 0
                for i in prvUser:
                    mone += 1
                check = False
                prvMsg = connection.recv(2048).decode()
                for i in Users:
                    if i == prvUser[0:len(prvUser) - 1]:
                        check = True  # If the user name exist change check so we send the prv msg to the username
                        break
                if check:
                    connection.send(("PRIVATE MESSAGE SENT TO " + prvUser[0:len(prvUser) - 1] + "!\n").encode())
                    Users[prvUser[0:len(prvUser) - 1]].send(("PRIVATE MESSAGE FROM " + prvMsg).encode())
                else:
                    connection.send(("USER NAME DOES NOT EXIST!\n").encode())
            else:
                for i in Users:
                    Users[i].send(message.encode())
        except:
            continue


def start():
    server.listen()
    while True:
        connection, addr = server.accept()
        thread = threading.Thread(target=newUser, args=(connection, addr))
        thread.start()


start()
