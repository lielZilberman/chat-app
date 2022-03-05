import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.simpledialog
import tkinter.scrolledtext
from tkinter import messagebox
import sys

# Explanation of how the whole system works is explained in our read me on our github repo.
# Getting address of the user
server = socket.gethostbyname(socket.gethostname())
port = 50000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# This function handles data which is received from the server
# The server sends specific strings each one is for a specific situation
def recvMsg(text_area):
    while True:
        try:
            message = client.recv(2048).decode()
            if message[0:19] == "%SHOW_SERVER_FILES%":
                fileList = message.split("~")
                messagebox.showinfo("SERVER FILES: ", fileList[1])
            elif message[0:13] == "DOWNLOAD_FILE":
                fileList = message.split("~")
                file = open(fileList[1], "wb")
                client.send("%GOT-ACK%".encode())
                image = client.recv(2048)
                while image:
                    file.write(image)
                    image = client.recv(2048)
                    if image == b"%IMAGE_COMPLETED%":
                        text_area.config(state='normal')
                        text_area.insert('end', "*FILE HAS BEEN SUCCESSFULLY DOWNLOADED!\n")
                        text_area.yview('end')
                        text_area.config(state='disabled')
                        break
                file.close()
            elif message[0:15] == "showUsersOnline":
                userOnline_list = message.split("~")
                mone = 0
                displayUsersOnline = ""
                for i in userOnline_list:
                    if mone != 0:
                        displayUsersOnline = displayUsersOnline + i + "\n"
                    mone += 1
                messagebox.showinfo("who's online", displayUsersOnline)
            else:
                text_area.config(state='normal')
                text_area.insert('end', message)
                text_area.yview('end')
                text_area.config(state='disabled')
        except:
            break


# connection close to the client which disconnected
# While this is true we might need to be able to receive messages or write messages


# Sends the entered message to the server
def input_text(username, message_text, to_text):
    text = f"{message_text.get('1.0', 'end')}"
    prvMsg = f"{to_text.get('1.0', 'end')}"
    # Send additional data to the server if it's a private message
    if len(prvMsg) > 1:
        client.send(("prvMsg" + prvMsg).encode())
    to_text.delete('1.0', 'end')
    message_text.delete('1.0', 'end')
    message_text.delete('1.0', 'end')
    client.send((username + ":" + " " + text).encode())


# Function to see which users are online
# sends a certain string to the server so the server can send the appropriate data
def online_func():
    client.send("showUsersOnline".encode())


# Functuion to remove the text in the text box
def clear_func(text_area):
    text_area.config(state='normal')
    text_area.delete('1.0', 'end')
    text_area.config(state='disabled')


# function
def on_closing(window, username):
    client.send(("disconnectUser~" + username).encode())
    window.destroy()
    client.close()
    sys.exit()


# Function which handles if the download button is pressed
def download(filename_text, saveas_text):
    fileName = f"{filename_text.get('1.0', 'end')}"
    saveAs = f"{saveas_text.get('1.0', 'end')}"
    client.send(("DOWNLOAD_FILE~" + fileName[0:len(fileName) - 1] + "~" + saveAs[0:len(saveAs) - 1]).encode("utf-8"))
    filename_text.delete('1.0', 'end')
    saveas_text.delete('1.0', 'end')


# Functions which handles if a entered username is already taken.
def is_taken(username):
    client.send("%CHECK_USERNAME%".encode())
    ack = client.recv(2048).decode()
    if ack == "ACK-RECEIVED":
        client.send(username.encode())
    userAccess = client.recv(2048).decode()
    if userAccess == "%USERNAME_DENIED%":
        return True
    else:
        return False


# Function which if the show files button is pressed
def showfiles():
    client.send("%SHOW_SERVER_FILES%".encode())


def start():
    mone = 0
    client.connect((server, port))
    username = tkinter.simpledialog.askstring("username", "enter your username ----------------------------->")
    checkAccess = is_taken(username)
    while checkAccess:
        username = tkinter.simpledialog.askstring("username has been taken",
                                                  "that username has already been taken, ""please choose another one: ")
        checkAccess = is_taken(username)
    window = tk.Tk()
    window.title("chat")
    canvas2 = tk.Canvas(window, width=800, height=600)
    canvas2.grid(columnspan=3, rowspan=3)
    welcome_label = tk.Label(window, text="welcome back, " + username + '!', relief="solid", font='Arial')
    welcome_label.place(x=300, y=20)
    message_label = tk.Label(window, text="message: ", font='Arial')
    message_label.place(x=20, y=500)
    message_text = tk.Text(window, width=20, height=1)
    message_text.place(x=120, y=507)
    text_area = tkinter.scrolledtext.ScrolledText(window)
    text_area.place(x=50, y=70)
    text_area.config(state='disabled')
    send_button = tk.Button(window, text="Send", bg='#20bebe', fg='white',
                            command=lambda: input_text(username, message_text, to_text))
    send_button.place(x=290, y=505)
    online_button = tk.Button(window, text="show online", bg='#20bebe', fg='white', command=lambda: online_func())
    online_button.place(x=600, y=23)
    clear_button = tk.Button(window, text="clear chat", bg='#20bebe', fg='white', command=lambda: clear_func(text_area))
    clear_button.place(x=675, y=23)
    logout_button = tk.Button(window, text="log out", bg='#20bebe', fg='white',
                              command=lambda: on_closing(window, username))
    if mone == 0:
        threadRecv = threading.Thread(target=recvMsg, args=(text_area,))
        threadRecv.start()
        mone += 1
    logout_button.place(x=30, y=23)
    download_button = tk.Button(window, text="Download", bg='#20bebe', fg='white',
                                command=lambda: download(filename_text, saveas_text))
    download_button.place(x=560, y=555)
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, username))
    showfiles_button = tk.Button(window, text="show server files", bg='#20bebe', fg='white',
                                 command=lambda: showfiles())
    showfiles_button.place(x=90, y=23)
    to_label = tk.Label(window, text="To: ", font='Arial')
    to_label.place(x=350, y=505)
    to_text = tk.Text(window, width=20, height=1)
    to_text.place(x=390, y=510)
    filename_label = tk.Label(window, text="server file name: ", font='Arial')
    filename_label.place(x=20, y=550)
    filename_text = tk.Text(window, height=1, width=15)
    filename_text.place(x=175, y=555)
    saveas_label = tk.Label(window, text="save as: ", font='Arial')
    saveas_label.place(x=350, y=550)
    saveas_text = tk.Text(window, height=1, width=15)
    saveas_text.place(x=430, y=555)
    window.mainloop()


def login():
    root = tk.Tk()
    root.title("chat")

    # canvas
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.grid(columnspan=3, rowspan=3)

    # logo
    logo = Image.open('ServerFiles/logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo)
    logo_label.image = logo
    logo_label.grid(column=1, row=0)

    # start button
    start_text = tk.StringVar()
    start_button = tk.Button(root, textvariable=start_text, command=lambda: start(), font='Arial', bg="#20bebe",
                             fg="white", height=2, width=15)
    start_text.set("LOGIN")
    start_button.grid(column=1, row=1)
    root.mainloop()


login()
