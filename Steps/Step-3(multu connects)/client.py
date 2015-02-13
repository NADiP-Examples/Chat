#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from threading import Thread


def receipt_data(sock):
    while True:
        data = sock.recv(1024)
        print(data)


sock = socket.socket()
sock.connect(('localhost', 9090))
th_receipt = Thread(target=receipt_data, args=(sock,))
th_receipt.start()
while True:
    message = input(': ')
    sock.send(message.encode())

sock.close()

