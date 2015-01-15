#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

#авторизация пользователя
# USER_NAME = input("Enter you name: ")
USER_NAME = 'user'

sock = socket.socket()
sock.connect(("127.0.0.1", 14900))

while True:
    message = input('You: ')
    message = "#%s:%s"%(USER_NAME, message)
    sock.send(message.encode())

# data = sock.recv(1024)
sock.close()

# print(data)