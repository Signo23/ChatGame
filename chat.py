#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 12:31:28 2021
@author: Lorenzo Signoretti
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

def receive():
    """Manage the recived messagges"""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")

            msg_list.insert(tkt.END, msg)
        except OSError:  
            break

def send(event=None):
    """Send message"""
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}": #La connessione viene chiusa
        client_socket.close()
        win.destroy()

"""La funzione che segue viene invocata quando viene chiusa la finestra della chat."""
def on_closing(event=None):
    """Invoked for close the window"""
    my_msg.set("{quit}")
    send()
    win.destroy()

win = tkt.Tk()
win.title("GameChat")

#Frame for messagges
messages_frame = tkt.Frame(win)
my_msg = tkt.StringVar()
my_msg.set("")
#scrollbar for prevoius messagges
scrollbar = tkt.Scrollbar(messages_frame)

# Contein messagges
msg_list = tkt.Listbox(messages_frame, height=25, width=125, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkt.Entry(win, textvariable=my_msg)
entry_field.bind("<Return>", send)

entry_field.pack()
send_button = tkt.Button(win, text="Invio", command=send)
send_button.pack()

win.protocol("WM_DELETE_WINDOW", on_closing)

#----Connessione al Server----
HOST = 'localhost'
PORT = 53000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkt.mainloop()
