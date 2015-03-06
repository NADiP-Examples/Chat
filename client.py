from tkinter import *
from tkinter.filedialog import *
import socket
from threading import Thread
from shortcuts import parser_command

# CONSTANTS
IP = '192.168.1.2'
PORT = 9090


def receive(conn):
    """Получает и выводит сообщение на экран"""
    while True:
        if not WORK:
            return
        conn.setblocking(0)
        try:
            message = SOCK.recv(1024).decode()
        except socket.error:  # данных нет
            continue
        message = parser_command(message)
        if isinstance(message, tuple):
            message = "send command %s \n" % message[0]
            # FIXME: некорректный код, переписать (подсказка: Обратить внимание на условие)
            display_message(message)
        else:
            display_message(message)
        tex.yview(END)


def enter_nickname():
    """Модельное окно ввода ника при коннекте на сервер"""
    def send_nick(event):
        nick_name = ent_nick.get()
        label['text'] = nick_name
        SOCK.send(nick_name.encode())
        win.destroy()

    win = Toplevel()
    win.resizable(False, False)
    Label(win, text="Enter nickname").pack()
    ent_nick = Entry(win)
    ent_nick.pack()
    but_send_nick = Button(win, text="Ok")
    but_send_nick.pack()
    but_send_nick.bind('<Button-1>', send_nick)
    ent_nick.bind('<Return>', send_nick)
    # Захватываем фокус
    win.focus_set()
    # Скрываем основное окно
    root.withdraw()
    # Ждем закрытия данного окна
    win.wait_window()
    # Показываем основное окно
    root.deiconify()


def add_nick(nick):
    list_box.insert(1, "Вася")
    list_box.insert(2, "Петя")
    list_box.insert(3, "Коля")


def remove_nick(nick):
    pass


def send(event):
    """bind: Отправляет сообщение на сервер"""
    if SOCK:
        s = ent.get()
        ent.delete(0, END)
        SOCK.send(s.encode())


def display_message(message):
    """Выаодит соотщение"""
    parse_res = parse_smiles(message)
    # print(parse_res)
    if parse_res:
        tex.insert(END, parse_res[0])
        tex.image_create(END, image=parse_res[1])
        tex.insert(END, parse_res[-1]+"\n")
    else:
        tex.insert(END, message+"\n")


def parse_smiles(message):
    """Парсим смайлы"""
    # print("mes: %s" % message)
    for txt_smile in SMILES.keys():
        if txt_smile in message:
            cut_string = message.partition(txt_smile)
            return cut_string[0], SMILES[txt_smile], cut_string[-1]


def on_close():
    """ Перехват события "Закрытие окна" """
    global WORK
    print("Close Window")
    WORK = False
    root.quit()


def connect_to_server(event):
    """ bind """
    global SOCK
    SOCK = socket.socket()
    SOCK.connect((IP, PORT))
    SOCK.setblocking(0)
    th1 = Thread(target=receive, args=(SOCK,))
    th1.start()
    enter_nickname()


def private_message(e):
    """ bind """
    # indexes = list_box.curselection()
    list_box_values = [list_box.get(idx) for idx in list_box.curselection()]
    print(list_box_values)

root = Tk()

# GLOBALS
WORK = True  # Работает ли клиент (чтобы убить все потоки клиента, при закрытии окна)
SOCK = None  # Соккет подключения к серверу
SMILES = {':-)': PhotoImage(file='img/Smile.gif'), '^-^': PhotoImage(file='img/a115.gif')}

# MAIN
content_frame = Frame(root, bg='blue', bd=1)
text_frame = Frame(content_frame, bg='blue', bd=1)
input_frame = Frame(root, bg='blue', bd=1)
tex = Text(text_frame,)
but = Button(input_frame, text='Отправить')
but_conn = Button(root, text="Connect")
label = Label(input_frame, text="new")
list_box = Listbox(content_frame)
ent = Entry(input_frame, width=80)
scr = Scrollbar(text_frame, command=tex.yview)
tex.configure(yscrollcommand=scr.set)

content_frame.pack(fill='both')
text_frame.pack(side='left', fill='both')
tex.pack(side='left', fill='both')
scr.pack(side='right', fill='both')
list_box.pack(side='right', fill='both')

input_frame.pack(fill='both')
label.pack(side='left', fill='both')
ent.pack(side='left', expand=True, fill='both')
but.pack(side='left')
but_conn.pack(side=TOP)

but.bind('<Button-1>', send)
but_conn.bind('<Button-1>', connect_to_server)
ent.bind('<Return>', send)
list_box.bind('<Double-Button-1>', private_message)

add_nick('new')

root.protocol("WM_DELETE_WINDOW", on_close)
mainloop()