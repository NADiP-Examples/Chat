#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from threading import Thread


def connect(conn, addr):
    while True:
        data = conn.recv(1024)
        print(data.decode())
        if not data:
            break
        # conn.send(data.upper())
        for client in clients_list:
            client.send(data)

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
clients_list = []

while True:
    conn, addr = sock.accept()
    clients_list.append(conn)
    th = Thread(target=connect, args=(conn,addr))
    print('connected:', addr)
    th.start()
