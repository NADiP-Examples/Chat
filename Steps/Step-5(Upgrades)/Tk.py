from tkinter import *
import socket

from threading import Thread

def recv(sock):
    # Получает и выводит сообщение на экран
    while True:
        if th1.is_alive():
            return
        message1=sock.recv(1024)
        tex.insert(END,message1.decode()+"\n")

def send(event):
    # Отправляет сообщение на сервер.
    s = ent.get()
    ent.delete(0,END)
    sock.send(s.encode())

def on_close():
    print("Close Window")
    th1.join()
    root.quit()

def dialog():
    win = Toplevel()
    Label(win, text = "Новое окно").pack()
    photo = PhotoImage(file="avatar-small.png")
    Button(win, text = "Ok", image=photo).pack()
    win.focus_set()
    win.grab_set()
    win.wait_window()
    print("dialog exit")

sock = socket.socket()                                      #Создаёт сокет
sock.connect(('127.0.0.1', 9090))                           #Подключается к серверу

root=Tk()
tex=Text(root,)                                             #Создаёт экран, куда будет выводится сообщение
tex.pack(fill='both')
but=Button(root,text='Отправить')                           #Создаёт кнопку "Отправить"
but.pack(side='right')
ent=Entry(root,width=100)                                   #Создаёт строку для ввода
ent.pack(side='left')

but.bind('<Button-1>',send)
root.protocol("WM_DELETE_WINDOW", on_close)
th1=Thread(target=recv,args=(sock,))
th1.start()

mainloop()
