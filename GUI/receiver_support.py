#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 6.1
#  in conjunction with Tcl version 8.6
#    May 20, 2021 03:37:04 AM CEST  platform: Windows NT

import sys
import os
import figureGen
import pandas as pd
import socket
import select
import pickle
# from io import StringIO
import datetime
import tkinter as tk
import tkinter.font as Tkfont
import tkinter.ttk as ttk
    


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

    # --- Start of init edit ---
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]

    global target
    target = figureGen.Target([3, 4, 5, 51], totalSize=1.25)

    global HOST, PORT
    HOST = '192.168.1.4'
    PORT = 12345

    # Create default image
    update_img(point=None, defaultImg=True)

    root.bind('<Tab>', lambda e: open_input("shooter name"))

    root.after(2000, socket_connect)

    # root.after(500, open_input, "shooter name")
    # root.after(500, open_input, "date")
    # --- End of init edit ---




def update_img(point, clock=None, defaultImg=False):
    if defaultImg:
        target.default()
    else:
        try:
            target.targetHit(int(point), clock)
        except ValueError:
            target.targetHit(point, clock)
    target.saveFigure(dpi=180)
    photo_location = os.path.join(prog_location,"./image.png")
    global _img0
    _img0 = tk.PhotoImage(file=photo_location)
    w.Image.configure(image=_img0)

    if not defaultImg:
        root.update()   #! This might not be needed
        root.after(3000) #! Image stays for at least 1.5s before changing

"""
    Begining of socket functions
"""

def socket_connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    open_popup()
    while True:
        try:
            s.connect((HOST, PORT))
            s.setblocking(0)
            break
        except TimeoutError:
            print("Waiting to connect!")
    print("Connected")
    close_popup()
    root.after(300, open_input, "shooter leader name")
    root.after(2000, socket_recive)
    root.after(5000, ping)


def socket_send(data, data_info):
    data_info = data_info.lower()
    if len(str(data_info)) > 8:
        raise ValueError("Data_info has to be max 8 characters, was: " + str(len(data_info)))
    data_info = f'{data_info: <8}'

    size = len(data) + len(data_info) + 2   # 2 is for "packet_len"
    FULL_BYTE = int(0xFF)
    packet_len = bytes([size//FULL_BYTE, size % FULL_BYTE]) # Returns two bytes to store the packet size excluding bytes for TCP protocoll
    prefix = packet_len + data_info.encode()
    print(len(prefix + data))
    try:
        s.sendall(prefix + data)
    except (ConnectionResetError, ConnectionAbortedError) as e:
        print(e)
        socket_connect()
        socket_send(data, data_info)


def socket_recive():
    # print("Reciveing")
    FULL_BYTE = int(0xFF)
    msg = b''
    msg_list = []
    length = 0
    has_read = False
    while True:
        r,w,e = select.select([s], [], [], 0.2)
        if r:
            try:
                msg += s.recv(2048)
                has_read = True
            except (ConnectionResetError, ConnectionAbortedError) as e:
                print(e)
                socket_connect()

        if len(msg) >= 2:

            if length == 0:
                length = int(msg[0])*FULL_BYTE + int(msg[1]) # Convert first 2 bytes to decimal
                print(length)

            if len(msg) >= length and length:
                data_info = msg[2:10]
                data = msg[10:length]
                msg_list.append((data, data_info.decode().strip()))
                msg = msg[length:]
                length = 0

        if not len(msg):
            root.after(500, socket_recive)
            if has_read:
                act_on_msg(msg_list)
            return

def ping():
    socket_send(b'', "ping")
    root.after(5000, ping)

"""
    End of socket functions
"""

def act_on_msg(msg_list):
    while msg_list:
        pickled_data, data_info = msg_list.pop(0)

        if data_info == "name":
            name = pickled_data.decode()
            w.shooter_lables[0].configure(text=name)

        elif data_info == "shooter":
            data = pickle.loads(pickled_data)
            data.seek(0)
            shooter_df = pd.read_csv(data, index_col=0)
            print(shooter_df)            

            row_list = format_dataframe(shooter_df)
            i=0
            for label in w.shooter_lables[1:]:
                txt = row_list[i]
                label.configure(text=txt)
                i += 1

        elif data_info == "log_df":
            data = pickle.loads(pickled_data)
            data.seek(0)
            log_df = pd.read_csv(data, index_col=0)
            print(log_df)
            fill_listbox(log_df)

        elif data_info == "new_hit":
            point, clock = pickle.loads(pickled_data)
            if clock is None:
                update_img(point)
            else:
                update_img(point, int(clock))

        else:
            print("Unrecognizeable info: " + data_info)
            print("Was carrying this data: " + str(pickled_data))


def format_dataframe(df):
    df = df.fillna('-')
    for key in ['St', 'J', 'L', 'D']:
        df[key] = df[key].astype(str)
        df[key] = df[key].str.split('.')
        df[key] = df[key].str[0]

    row_list = pd.DataFrame(df).to_string(
        index=False,
        justify='center',
        formatters={
            "St": "{:^5}".format,
            "J": "{:^5}".format,
            "L": "{:^5}".format,
            "D": "{:^5}".format,
        }
        ).splitlines()
    return row_list


def fill_listbox(df):
    w.Listbox1.delete(0,'end')
    df = df.where(pd.notnull(df), None)
    for row in df.values:
        name = row[0]
        style = row[1]
        point = str(row[2])
        clock = row[3]

        if name == None:
            if clock == None:
                string = point
            else:
                string = "{} kl {:.0f}".format(point, clock)
        else:
            if clock == None:
                string = "{}: [{}] {}".format(name.split()[0], style, point)
            else:
                string = "{}: [{}] {} kl {:.0f}".format(name.split()[0], style, point, clock)
        w.Listbox1.insert('end', string)
    w.Listbox1.see(0)




class Popup(tk.Toplevel):
    """modal window requires a master"""
    def __init__(self, master, **kwargs):
        tk.Toplevel.__init__(self, master, **kwargs)
        # self.overrideredirect(True)
        self.geometry('320x100+500+500') # set the position and size of the popup

        lbl = tk.Label(self, text="Försöker koppla til markördatorn ... ", font=("Segoe UI", 11, "bold"))
        lbl.place(relx=.5, rely=.5, anchor='c')
        self.title("Connecting...")

        # The following commands keep the popup on top.
        # Remove these if you want a program with 2 responding windows.
        # These commands must be at the end of __init__
        self.transient(master) # set to be on top of the main window
        self.grab_set() # hijack all commands from the master (clicks on the main window are ignored)

def open_popup():
    root.popup = Popup(root)
    root.update()

def close_popup():
    root.popup.destroy()


class InputPopup(tk.Toplevel):
    """modal window requires a master"""
    def __init__(self, master, input_type, **kwargs):
        tk.Toplevel.__init__(self, master, **kwargs)
        self.geometry('320x150+500+500')
        self.title("Connecting...")

        self.input_type = input_type

        self.lbl = tk.Label(self, font=("Segoe UI", 11))
        self.lbl.place(relx=.5, rely=.3, anchor='c')

        self.entry = tk.Entry(self, font=("Segoe UI", 11))
        self.entry.place(relx=.5, rely=.6, anchor='c')
        self.entry.bind('<Key-Return>', self.verify_entry)
        self.entry.focus()

        self.lbl_entry_error = tk.Label(self)
        self.lbl_entry_error.place(relx=.5, rely=.75, anchor='c')
        self.lbl_entry_error.configure(activebackground="#f9f9f9")
        self.lbl_entry_error.configure(activeforeground="black")
        # self.lbl_entry_error.configure(background="#d9d9d9")
        self.lbl_entry_error.configure(disabledforeground="#a3a3a3")
        self.lbl_entry_error.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.lbl_entry_error.configure(foreground="#ff0000")
        self.lbl_entry_error.configure(highlightbackground="#d9d9d9")
        self.lbl_entry_error.configure(highlightcolor="black")
        self.lbl_entry_error.configure(text='''Invalid''')

        self.lbl_entry_error_location = self.lbl_entry_error.place_info()
        self.lbl_entry_error.place_forget()



        if input_type == "shooter name":
            self.lbl.configure(text="Mata in namn, tex. (John Doe)")
            self.entry.bind('<Escape>', lambda e: self.destroy())

        elif input_type == "shooter leader name":
            self.lbl.configure(text="Mata in skytte ledarens namn, tex. (L-O Nilsson)")

        elif input_type == "date":
            self.lbl.configure(text="Datum, (YYYY-MM-DD)")

        else:
            raise ValueError(input_type)
        
        self.transient(master)
        self.grab_set()
        self.focus_force()

    def send_entry(self, data_info):
        data_bytes = self.entry.get().encode()
        socket_send(data_bytes, data_info)
        self.destroy()

    def verify_entry(self, _):
        self.lbl_entry_error.place_forget()
        input = self.entry.get()
        type = self.input_type  #! "type" is not a good variable name

        if type in ["shooter name", "shooter leader name"]:
            
            if len(input.split()) < 2:
                print("Ska ha för- och efternamn", flush=True)
                self.lbl_entry_error.place(
                    relx=self.lbl_entry_error_location['relx'],
                    rely=self.lbl_entry_error_location['rely'],
                    anchor='c'
                )

            else:
                if type == "shooter leader name":
                    open_input("date")
                self.send_entry(type.split()[1])

        elif type == "date":
            try:
                datetime.datetime.strptime(input, "%Y-%m-%d")
                print("This is the correct date string format.")
                self.send_entry(type)
            except ValueError:
                print(f'{input} is the incorrect date string format. It should be YYYY-MM-DD', flush=True)
                self.lbl_entry_error.place(
                    relx=self.lbl_entry_error_location['relx'],
                    rely=self.lbl_entry_error_location['rely'],
                    anchor='c'
                )


def open_input(input_type):
    # input_type is one of "shooter name", "shooter leader name" or "date"
    root.input = InputPopup(root, input_type)
    root.update()

def close_input():
    root.input.destroy()


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import receiver
    receiver.vp_start_gui()




