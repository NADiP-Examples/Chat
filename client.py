from tkinter import *
from tkinter.filedialog import *
import socket
from threading import Thread
from shortcuts import parser_command

# CONSTANTS
IP = '127.0.0.1'
PORT = 9090


def smile_insert(event):
    ent.insert(END, event.widget.smile_text)


def smiles_window(e):
    """ bind - open 'smiles window' """
    smiles_win = Toplevel()
    smiles_win.resizable(False, False)
    smiles_win.wm_title("Select smiles")
    for el in SMILES.keys():
        but_smiles = Button(smiles_win,image=SMILES[el])
        but_smiles.pack(side='left')
        but_smiles.bind('<Button-1>', smile_insert)
        but_smiles.smile_text = el


def receive(conn):
    """Получает и выводит сообщение на экран"""
    while True:
        if not WORK:
            return
        conn.setblocking(0)
        try:
            message = SOCK.recv(1024).decode()
            # print(message)
        except socket.error:  # данных нет
            continue
        message = parser_command(message)
        if isinstance(message, tuple):
            command, value = message
            if command == 'nickadd':
                add_nick(value)
            if command == 'nickdelete':
                # print(command, value)
                remove_nick(value)
            if command == 'listnicks':
                # print(value)
                add_nicks(value.split(','))
            message = "send command %s \n" % message[0]
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


def add_nicks(list_nicks):
    # Добавляет ники, которые были до подключения клиента к серверу
    for nick in list_nicks:
        add_nick(nick)


def add_nick(nick):
    # Добавляет ник в список
    list_box.insert(END, nick)


def remove_nick(nick):
    # Удаляет ник из списка
    elements = list_box.get(0, list_box.size())
    idx = elements.index(nick)
    list_box.delete(idx)


def send(event):
    """bind: Отправляет сообщение на сервер"""
    if SOCK:
        s = ent.get()
        ent.delete(0, END)
        SOCK.send(s.encode())


def display_message(message):
    """Выаодит соотщение"""
    parse_res = parse_smiles(message)
    if parse_res:
        for el in parse_res:
            if isinstance(el, PhotoImage):
                tex.image_create(END, image=el)
                continue
            tex.insert(END, el)
        tex.insert(END, '\n')
    else:
        tex.insert(END, message+"\n")


def parse_smiles(message):
    """Парсим смайлы"""
    sta = [message]
    for txt_smile in SMILES.keys():
        sta = parse(sta, txt_smile)
    for ind, el in enumerate(sta):
        for txt_smile in SMILES.keys():
            if el==txt_smile:
                sta[ind] = SMILES[txt_smile]
    return sta


def parse(lt, sml):
    pl = []
    crt = []
    if lt==[]:
        return []
    for st in lt:
        ar = list(st.partition(sml))
        while (sml in ar[-1]) and (ar[-1]!=sml):
            crt = list(ar[-1].partition(sml))
            ar.pop(-1)
            for el in crt:
                if el=='':
                    continue
                ar.append(el)
        for el in ar:
            if el=='':
                continue
            pl.append(el)
    return pl


def on_close():
    """ Перехват события "Закрытие окна" """
    global WORK
    print("Close Window")
    WORK = False
    root.quit()


def connect_to_server(event=None):
    """ bind """
    global SOCK
    SOCK = socket.socket()
    SOCK.connect((IP, PORT))
    SOCK.setblocking(0)
    th1 = Thread(target=receive, args=(SOCK,))
    th1.start()
    enter_nickname()


def private_message(events):
    """ bind """
    # indexes = list_box.curselection()
    list_box_values = [list_box.get(idx) for idx in list_box.curselection()]
    print(list_box_values)

root = Tk()
root.resizable(False, False)

m = Menu(root)
root.config(menu=m)

fm = Menu(m)                                #создается пункт меню с размещением на основном меню (m)
m.add_cascade(label="Меню", menu=fm)         #пункту располагается на основном меню (m)
fm.add_command(label="Connect", command=connect_to_server)

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
label = Label(input_frame, text="new")
list_box = Listbox(content_frame)
ent = Entry(input_frame, width=80)
scr = Scrollbar(text_frame, command=tex.yview)
tex.configure(yscrollcommand=scr.set)
but_sm=Button(input_frame,text='Smile')

content_frame.pack(fill='both')
text_frame.pack(side='left', fill='both')
tex.pack(side='left', fill='both')
scr.pack(side='right', fill='both')
list_box.pack(side='right', fill='both')
but_sm.pack(side='right')

input_frame.pack(fill='both')
label.pack(side='left', fill='both')
ent.pack(side='left', expand=True, fill='both')
but.pack(side='left')

but_sm.bind('<Button-1>',smiles_window)
but.bind('<Button-1>', send)
ent.bind('<Return>', send)
list_box.bind('<Double-Button-1>', private_message)


root.protocol("WM_DELETE_WINDOW", on_close)
mainloop()