import socket
from threading import Thread


def connect(conn, clients):
    # Получает сообщение и отправляет его всем клиентам
    while True:
        try:
            data = conn.recv(1024)
            data = data.decode()
            Nduplicate='#nickduplicate:'
            if data in g_nicks:
                conn.send(Nduplicate.encode())
            else:
            # Определение первого сообщения подключившегося клиента
                if not (conn in clients):
                    clients.append(conn)  # Добавление в список клиентов
                    g_nicks.append(data)  # Добавление в список ников

                    # Рассылка информации об добавлении клиента в панель "Ников"
                    nick_send = data
                    nick_send = '#nickadd:' + nick_send
                    for el in clients:
                        el.send(nick_send.encode())

                    welcome_message = "Welcome, %s" % data
                    conn.send(welcome_message.encode())
                else:

                    num_conn = clients.index(conn)
                    nick_send = "%s:%s" % (g_nicks[num_conn], data)
                    # nick_send = nick[num_conn]
                    # nick_send = nick_send+':'
                    # nick_send = nick_send+data

                    for el in clients:
                        el.send(nick_send.encode())
            # Отключения клиента без ошибки
        except (ConnectionResetError, BrokenPipeError):
                    print('disconnected')
                    num_conn = clients.index(conn)
                    nick_send = g_nicks[num_conn]
                    g_nicks.remove(nick_send)  # Удаление из списка ников
                    clients.remove(conn)  # Удаление из списка подключений
                    # Рассылка информации об удалении клиента из панели "Ников"
                    for el in clients:
                        nick_send = '#nickdelete:'+nick_send
                        el.send(nick_send.encode())
                    return

# GLOBALS
g_nicks = []

# MAIN
sock = socket.socket()
sock.bind(("", 9090))
sock.listen(1)
clients = []  # FIXME:Действительно ли нужен глобальный список, если он используется только в колальной области функции?
last_massageX4 = []

while True:
    conn, addr = sock.accept()
    print('connected:', addr)
    th = Thread(target=connect, args=(conn, clients))
    th.start()
