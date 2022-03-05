import threading
import socket
import sys
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Basic chat room via terminal.
# So if someone wants to private message someone , he will have to write private and then the name of the user
# Each user's IP will be identified with his user name.
# A list to keep to clients connections socket objects.
format = "utf-8"
Users = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddr = socket.gethostbyname(socket.gethostname())
serverPort = 5050
server.bind((serverAddr, serverPort))


def newUser(connection, addr):
    # connection.send("Enter username (only letters and numbers): ".encode())
    # clientUserName = connection.recv(2048).decode()
    # print("The clients user name: ",clientUserName)
    denied = True
    userName = ""
    while denied:
        try:
            check = False
            message = connection.recv(2048).decode()
            connection.send("ACK-RECEIVED".encode())
            userName = connection.recv(2048).decode()
            print("message= ", message)
            print("userName= ", userName)
            for i in Users:
                if userName == i:
                    print("user denied")
                    connection.send(("%USERNAME_DENIED%").encode())
                    check = True
            if check:
                continue
            connection.send("APPROVED".encode())
            denied = False
        except:
            continue
    for i in Users:
        print("Users= ", i)
        Users[i].send(("*" + userName + " Has CONNECTED to the chat!*\n").encode())
    Users[userName] = connection
    connection.send(("*You have been CONNECTED to the chat!*\n").encode())
    while True:
        try:
            message = connection.recv(2048).decode()
            mone = 0
            for i in message:
                print("char at index {0} is {1}".format(mone, i))
                mone += 1
            if message == "%SHOW_SERVER_FILES%":
                send_data = ""
                print("WASSUP")
                files = os.listdir("ServerFiles")
                if len(files) == 0:
                    print("LENGTH IS == 0")
                    connection.send("%SHOW_SERVER_FILES%~Server has no FILES".encode())
                else:
                    send_data += "\n".join(f for f in files)
                    print("send data= ", send_data)
                    connection.send(("%SHOW_SERVER_FILES%~" + send_data).encode())
            elif message[0:13] == "DOWNLOAD_FILE":
                fileList = message.split("~")
                print("file name= 1 ", fileList[1])
                print("file name= 1 ", fileList[2])
                print("open= ServerFiles/" + fileList[1])
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
                            print("Still sending")
                        connection.send(b"%IMAGE_COMPLETED%")
                        print("DONE SNEIDNG!")
                        file.close()
                except:
                    connection.send("Failed to download file\n".encode())
                    continue
            elif message[0:14] == "disconnectUser":
                print("User disconnected")
                connection.close()  # Closing client's socket
                discList = message.split("~")
                Users.pop(discList[1])  # Removing from the dictionary
                for i in Users:
                    Users[i].send(("*" + userName + " Has DISCONNECTED from the chat!*\n").encode())
                sys.exit()  # Closing thread
                # print("Updated connections = {0}".format(threading.activeCount() - 1))  # reducing the thread of main
            elif message == "showUsersOnline":
                usersOnline = "showUsersOnline"
                for i in Users:
                    usersOnline = usersOnline + "~" + i
                connection.send(usersOnline.encode())
            elif message[0:6] == "prvMsg":
                prvUser = message[6:]
                mone = 0
                for i in prvUser:
                    print("char at index {0} is {1}".format(mone, i))
                    mone += 1
                print(message)
                prvMsg = connection.recv(2048).decode()
                print("The actual message= ", prvMsg)
                # Users[prvUser].send(("PRIVATE MESSAGE SENT TO "+prvMsg).encode())
                connection.send(("PRIVATE MESSAGE SENT TO " + prvUser[0:len(prvUser) - 1] + "!\n").encode())
                Users[prvUser[0:len(prvUser) - 1]].send(("PRIVATE MESSAGE FROM " + prvMsg).encode())
            else:
                print("Maybe worked")
                for i in Users:
                    Users[i].send(message.encode())
                # Later do that the server sends the message for everyone except the sender
        except:
            continue
    # #Here ill have to check if this user name already exists.
    # print(userName)
    print("addr= ", addr)


def start():
    server.listen()
    while True:
        connection, addr = server.accept()
        print("Address of the user connected= ", addr)
        thread = threading.Thread(target=newUser, args=(connection, addr))
        thread.start()
        print("active connections = {0}".format(threading.activeCount() - 1))  # reducing the thread of main


start()
