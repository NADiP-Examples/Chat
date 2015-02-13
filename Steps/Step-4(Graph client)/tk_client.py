#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
from tkinter import *

IP = "127.0.0.1"
PORT = 9090


class ButSend():
    def __init__(self, parent, text_field):
        self.but = Button(parent)
        self.but["text"] = "Send"
        self.but.bind("<Button-1>", self.printer)
        self.but.pack(side=RIGHT)
        self.text = text_field

    def printer(self, event):
        message = self.text.get()
        self.text.delete(0, END)
        message = "#%s:%s"%(USER_NAME, message)
        sock.send(message.encode())
        print()


def get_data_from_server():
    sock.connect((IP, PORT))
    while True:
        data = sock.recv(1024)
        text.insert(END, data.decode()+'\n')

# авторизация пользователя
# USER_NAME = input("Enter you name: ")
USER_NAME = 'user'

root = Tk()

scrollbar = Scrollbar(root)
text = Text(root, width=40, height=20, font='14')
ent = Entry(root, width=40, bd=3)

scrollbar.pack(side=RIGHT, fill=Y)
text.pack()
ent.pack()

but_send = ButSend(parent=root, text_field=ent)
ent.bind('<Return>', but_send.printer)


# scr = Scrollbar(root, command=tx.yview)
text.configure(yscrollcommand=scrollbar.set)


sock = socket.socket()
# sock.connect(('localhost', 9090))

# Запускаем получение данных от сервера в отдельном потоке
# t = threading.Thread(target=get_data_from_server)
# t.daemon = True
# t.start()

root.mainloop()
