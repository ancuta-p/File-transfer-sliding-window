from tkinter import filedialog
from tkinter import *
from client import *
import threading


def select_file():
    select_th = threading.Thread(target=file_dialog)
    select_th.start()


def file_dialog():
    cl.update_idletasks()
    filename = filedialog.askopenfilename(title="Select file", filetypes=(('text files', 'txt'),))
    if filename:
        send_bttn.configure(state=NORMAL)
        refresh_bttn.configure(state=NORMAL)
        pkts_to_send(filename)


def sen():
    send_th = threading.Thread(target=send)
    ack_thread.start()
    send_th.start()
    send_bttn.configure(state=DISABLED)


def refresh():
    message.delete(1.0, END)
    f = open("clog.out", 'r')
    while True:
        text = f.readline()
        if not text:
            break
        message.insert(END, text)
    print(threading.enumerate())




cl = Tk()
cl.title("Client")
cl.geometry('620x480')
Label(cl,text="Protocol: Go-back-N").pack()
Label(cl,text="Window size: 4").pack()
Label(cl,text="PORT: 8080").pack()
message = Text(cl,  height=19, width=60)
scroll = Scrollbar(cl, command=message.yview)
scroll.pack(side=RIGHT, fill=Y)
message.configure(yscrollcommand=scroll.set)
message.pack(expand=TRUE)


info = ("Select a file, then START the server and SEND the file content"
      "\nThe file is split into packets and sent to the server"
      "\nPress REFRESH to see the transmission progress")

message.insert(END, info)

exit_button = Button(cl, text="Exit", command=quit, padx=10).pack(side=BOTTOM)
refresh_bttn = Button(cl, text="Refresh", command=refresh, state=DISABLED, padx=16)
refresh_bttn.pack(side=BOTTOM)
send_bttn = Button(cl, text="Send", command=sen, state=DISABLED, padx=22)
send_bttn.pack(side=BOTTOM)
file_bttn = Button(cl, text="Select file", command=select_file, padx=10).pack(side=BOTTOM)
cl.mainloop()
