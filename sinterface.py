import tkinter as tk
from tkinter import *
from server import *

import threading


def rec():
    #receive_th.daemon = True
    receive_th.start()
    send_bttn.configure(state=DISABLED)


def refresh():
    message.delete(1.0, END)
    f = open("slog.out",'r')
    while True:
        text = f.readline()
        if not text:
            break
        message.insert(END, text)


receive_th = threading.Thread(target=receive)
se = Tk()
se.title("Server")
se.geometry('620x480')
Label(se, text="Protocol: Go-back-N").pack()
Label(se, text="Window size: 4").pack()
Label(se, text="PORT: 7780").pack()
message = Text(se, height=20, width=60)
scroll = Scrollbar(se, command=message.yview)
scroll.pack(side=RIGHT, fill=Y)
message.configure(yscrollcommand=scroll.set)
message.pack(expand=TRUE)



exit_button = tk.Button(se, text="Exit", command=quit, padx=10).pack(side=BOTTOM)
refresh_bttn = Button(se, text="Refresh", command=refresh, state=NORMAL, padx=10)
refresh_bttn.pack(side=BOTTOM)
send_bttn = Button(se, text="Start", command=rec, state=NORMAL, padx=17)
send_bttn.pack(side=BOTTOM)


se.mainloop()
