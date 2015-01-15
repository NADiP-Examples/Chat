#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import socket

def parse(conn):# обработка соединения в отдельной функции
    data = conn.recv(1024)
    return data


sock = socket.socket()
sock.bind(("", 14900))
sock.listen(4)
sock.setblocking(0)
connects = [] #Все клиентские подлючения


while True:
    try:
        conn, addr = sock.accept()
        connects.append(conn)
        print('connect: %s. Num connected: %s'%(addr, len(connects)))
    except socket.error: # данных нет
        pass # тут ставим код выхода
    # finally:
    #     # так при любой ошибке
    #     # сокет закроем корректно
    #     print('close')
    #     sock.close()
    for conn in connects:
        try: data = parse(conn)
        except socket.error: # данных нет
            pass # тут ставим код выхода
        else: # данные есть
            print('data = ',data)
            for send_conn in connects:
                if conn == send_conn:
                    continue
                print('data sending')
                send_conn.send(data.upper())


