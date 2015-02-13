from tkinter import *

root = Tk()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

text = Text(root)
text.pack()

for i in range(100):
    text.insert(END, str(i)+"\n")

# attach listbox to scrollbar
text.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=text.yview)

mainloop()