#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, threading

IP = ""
PORT = 9090

class Connect(threading.Thread):
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        threading.Thread.__init__(self)
        print(self.addr, "...connected")
        ListClients[self.addr] = self.sock

    def run(self):
        while 1:
            try:
                buf = self.sock.recv(2048)
                print("!!!", self.addr,buf)
                print("data send")
                self.send_message_to_all(buf)

            except socket.error:
                # print(self.addr[0])
                # print(ListClients[self.addr][1])
                msg = "disconnected"
                print(msg)
                del ListClients[self.addr]
                print("all Clients = ", ListClients)
                break

    def send_message_to_all(self, message):
        for client in ListClients.values():
            print(message)
            print('client = ', client)
            client.send(message)

#Список клиентов
ListClients = {}

sock = socket.socket()
sock.bind((IP, PORT))
sock.listen(4)
connects = [] #Все клиентские подлючения


while True:
    conn, addr = sock.accept()
    Connect(conn, addr).start()


