import socket
from threading import Thread

def connect(conn,clients):
    # Получает сообщение и отправляет его всем клиентам
    while True:
        try:
            data=conn.recv(1024)
            for el in clients:
                el.send(data)
            print("I send data %s" % data)
        except ConnectionResetError:
            print('disconnected')
            clients.remove(conn)
            return




sock = socket.socket()
sock.bind(("", 9090))
sock.listen(1)
clients=[]


while True:
    conn, addr = sock.accept()
    clients.append(conn)
    print ('connected:', addr)
    th=Thread(target=connect, args=(conn,clients))
    th.start()
