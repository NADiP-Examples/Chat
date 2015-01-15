#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

#авторизация пользователя
# USER_NAME = input("Enter you name: ")
USER_NAME = 'user'

sock = socket.socket()
sock.connect(("127.0.0.1", 14900))
# sock.setblocking(0)

while True:
    data = sock.recv(1024)
    print(data)

# data = sock.recv(1024)
sock.close()

# print(data)