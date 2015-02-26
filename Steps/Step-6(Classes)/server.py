import socket
from threading import Thread


class ChatServer():
    def __init__(self, host="", port=9090):
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.clients = []

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            self.clients.append(conn)
            print('connected:', addr)
            th = Thread(target=self.client_connect, args=(conn, ))
            th.start()

    def client_connect(self, conn):
        """Получает сообщение и отправляет его всем клиентам"""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    raise ConnectionResetError
                for client in self.clients:
                    client.send(data)
                print("I send data %s" % data)
            except ConnectionResetError:
                print('disconnected')
                self.clients.remove(conn)
                return

server = ChatServer()
server.run()