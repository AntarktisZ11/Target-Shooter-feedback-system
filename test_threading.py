import threading
import socket
import tkinter as tk

def listen():
    with socket.socket() as s:
        s.bind(('localhost',0))
        s.listen(1)
        s.settimeout(5)
        s = s.accept()[0]
        s.shutdown()
        
t_listen = lambda:threading.Thread(target=listen).start()
        
root = tk.Tk()
# this is what you want to do using callbacks/queues . . .
tk.Button(root, text='threaded', command=t_listen).pack()

# . . . but this is what you are actually doing
tk.Button(root, text='sock block', command=listen).pack()
root.mainloop()