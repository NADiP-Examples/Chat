import socket
from tkinter import *
from threading import Thread


class Connect(Thread):
    def __init__(self, sock, output_widget):
        self.sock = sock
        self.sock.setblocking(0)
        self._alive = True
        self.output_widget = output_widget
        Thread.__init__(self)

    def run(self):
        while True:
            if not self._alive:
                return
            try:
                message = self.sock.recv(1024)
                self.display_message(message.decode())
            except socket.error:
                pass

    def display_message(self, message):
        parse_res = self.parse_smiles(message)
        if parse_res:
            self.output_widget.insert(END, parse_res[0])
            self.output_widget.image_create(END, image=parse_res[1])
            self.output_widget.insert(END, parse_res[-1]+"\n")
        else:
            self.output_widget.insert(END, message+"\n")

    def parse_smiles(self, message):
        for txt_smile in SMILES.keys():
            if txt_smile in message:
                cut_string = message.partition(txt_smile)
                # self.parse_smiles(cut_string[-1])
                return cut_string[0], SMILES[txt_smile], cut_string[-1]

    def kill(self):
        self._alive = False


def send(event):
    """Отправляет сообщение на сервер."""
    s = ent.get()
    ent.delete(0, END)
    sock.send(s.encode())
    text.yview(END)


def on_close():
    connect.kill()
    root.quit()


def dialog():
    win = Toplevel()
    win.resizable(False, False)
    Label(win, text="Enter nickname").pack()
    Entry(win).pack()
    Button(win, text="Ok").pack()
    # Захватываем фокус
    win.focus_set()
    # Захватываем все события
    win.grab_set()
    # Скрываем основное окно
    root.withdraw()
    # Ждем закрытия данного окна
    win.wait_window()
    # Показываем основное окно
    root.deiconify()

sock = socket.socket()
sock.connect(('127.0.0.1', 9090))

root = Tk()
root.resizable(False, False)
# Словарь для распарсивания смайлов
SMILES = {':-)': PhotoImage(file='images/Smile.gif'), '^-^': PhotoImage(file='images/a115.gif')}

content_frame = Frame(root, bg='green', bd=1)
text_frame = Frame(content_frame, bg='green', bd=1)
input_frame = Frame(root, bg='blue', bd=1)

text = Text(text_frame, )
but = Button(input_frame, text='Send')
label = Label(input_frame, text='nickName')
ent = Entry(input_frame)
list_box = Listbox(content_frame)

scr = Scrollbar(text_frame, command=text.yview)
text.configure(yscrollcommand=scr.set)

content_frame.pack(fill='both')
text_frame.pack(side='left', fill='both')
text.pack(side='left', fill='both')
scr.pack(side='right', fill='both')
list_box.pack(side='right', fill='both')

input_frame.pack(fill='both')
label.pack(side='left', fill='both')
ent.pack(side='left', expand=True, fill='both')
but.pack(side='left')


but.bind('<Button-1>', send)
ent.bind('<Return>', send)

root.protocol("WM_DELETE_WINDOW", on_close)

connect = Connect(sock, text)
connect.start()

# dialog()
mainloop()
