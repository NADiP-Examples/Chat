from tkinter import *
import socket, threading

IP = "127.0.0.1"
PORT = 14900

class But_send:
    def __init__(self, parent, text_field):
        self.but = Button(parent)
        self.but["text"] = "Send"
        self.but.bind("<Button-1>",self.printer)
        self.but.grid(row=1, column=1)
        self.text = text_field

    def printer(self,event):
        message = self.text.get()
        self.text.delete(0, END)
        message = "#%s:%s"%(USER_NAME, message)
        sock.send(message.encode())
        print()


def get_data_from_server():
    sock.connect((IP, PORT))
    while True:
        data = sock.recv(1024)
        tx.insert(END, data.decode()+'\n')


#авторизация пользователя
USER_NAME = input("Enter you name: ")
# USER_NAME = 'user'

root = Tk()
 
tx = Text(root,width=40, height=20, font='14')
ent = Entry(root,width=40,bd=3)
scr = Scrollbar(root,command=tx.yview)
tx.configure(yscrollcommand=scr.set)
but_send = But_send(parent=root, text_field=ent)
 
tx.grid(row=0,column=0)
scr.grid(row=0,column=1)
ent.grid(row=1, column=0)
ent.bind('<Return>',but_send.printer)

sock = socket.socket()

# Запускаем получение данных от сервера в отдельном потоке
t = threading.Thread(target=get_data_from_server)
t.daemon = True
t.start()

root.mainloop()








# while True:
#     message = input('You: ')
#     message = "#%s:%s"%(USER_NAME, message)
#     sock.send(message.encode())
#
# # data = sock.recv(1024)
# sock.close()