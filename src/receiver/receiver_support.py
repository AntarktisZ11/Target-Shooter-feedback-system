#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 6.1
#  in conjunction with Tcl version 8.6
#    May 20, 2021 03:37:04 AM CEST  platform: Windows NT

# Standard Library
import datetime
import os
import pickle
import sys
import tkinter as tk
from abc import ABC, abstractmethod
from enum import Enum, auto

# Third-Party
import pandas as pd

# First-Party
import figureGen
from socket_stuff import ReceiverSocket


# def init(top: tk.Tk, gui: receiver.Toplevel1, *args, **kwargs): # ! Only when coding
def init(top: tk.Tk, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

    # --- Start of init edit ---
    global PROG_LOCATION
    prog_call = sys.argv[0]
    PROG_LOCATION = os.path.split(prog_call)[0]

    global target
    target = figureGen.Target([3, 4, 5, 51], totalSize=1.25, dpi=180)

    # Create default image
    update_img_default()

    root.bind("<Tab>", lambda e: open_input(InputType.SHOOTER_NAME))
    root.bind("<Tab>", lambda e: print("Tab"), add=True)
    root.bind("<FocusOut>", lambda e: prevent_focus_out())

    global socket
    socket = ReceiverSocket.ReceiverSocket(root, act_on_msg)

    # --- End of init edit ---


def prevent_focus_out():
    print("FocusOut")

    if is_popup_open():
        return
    if is_input_open():
        return

    print("root.focus_force()")
    root.after(1, lambda: root.focus_force())


def is_popup_open():
    return hasattr(root, "popup") and root.popup.winfo_exists()


def is_input_open():
    return hasattr(root, "input") and root.input.winfo_exists()


def update_img(point, clock=None):
    if clock is None:
        photo_location = os.path.join(PROG_LOCATION, "images", f"./{point}.png")
    else:
        photo_location = os.path.join(PROG_LOCATION, "images", f"./{point}_{clock}.png")

    if not os.path.exists(photo_location):
        print("Creating new photo")
        try:
            target.targetHit(int(point), clock)
        except ValueError:
            target.targetHit(point, clock)

    global _img0
    _img0 = tk.PhotoImage(file=photo_location)

    w.Image.configure(image=_img0)

    root.update_idletasks()
    root.after(5000)  # ! Image stays for at least 3s before changing


def update_img_default():
    # global photo_location
    photo_location = os.path.join(PROG_LOCATION, "images", "./default.png")
    if not os.path.exists(photo_location):
        target.default()  # ! After this 'photo_location' will exist

    global _img0
    _img0 = tk.PhotoImage(file=photo_location)

    w.Image.configure(image=_img0)


def act_on_msg():
    while socket.msg_list:
        pickled_data, data_info = socket.msg_list.pop(0)

        if data_info == "name":
            name = pickled_data.decode()
            w.Label_Shooter_Name.configure(text=name)

        elif data_info == "shooter":
            data = pickle.loads(pickled_data)
            data.seek(0)
            shooter_df = pd.read_csv(data, index_col=0)
            print(shooter_df)

            shooter_df = format_dataframe(shooter_df)
            df_row_col_list = [shooter_df.columns.values]
            df_row_col_list.extend(shooter_df.values)
            i = 0
            for label in w.shooter_labels:
                row = i // 4
                col = i % 4
                label.configure(text=df_row_col_list[row][col])
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


def format_dataframe(df: pd.DataFrame):
    df = df.fillna("-")
    for key in ["St", "J", "L", "D"]:
        df[key] = df[key].astype(str)
        df[key] = df[key].str.split(".")
        df[key] = df[key].str[0]
    return df


def fill_listbox(df: pd.DataFrame):
    w.Listbox1.delete(0, "end")
    df = df.where(pd.notnull(df), None)
    for row in df.values:
        name = row[0]
        style = row[1]
        point = str(row[2])
        clock = row[3]

        if name is None:
            if clock is None:
                string = " " + point
            else:
                string = " {} kl {:.0f}".format(point, clock)
        else:
            if clock is None:
                string = " {}: [{}] {}".format(name.split()[0], style, point)
            else:
                string = " {}: [{}] {} kl {:.0f}".format(name.split()[0], style, point, clock)
        w.Listbox1.insert("end", string)
    w.Listbox1.see(0)


class NetworkPopup(tk.Toplevel):
    """window requires a master"""

    def __init__(self, master, **kwargs):
        tk.Toplevel.__init__(self, master, **kwargs)
        # self.overrideredirect(True)
        self.geometry("320x100+500+500")  # set the position and size of the popup

        lbl = tk.Label(self, text="Försöker koppla till markördatorn ... ", font=("Segoe UI", 11, "bold"))
        lbl.place(relx=0.5, rely=0.5, anchor="c")
        self.title("Connecting...")

        # The following commands keep the popup on top.
        # Remove these if you want a program with 2 responding windows.
        # These commands must be at the end of __init__
        self.transient(master)  # set to be on top of the main window
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)


def open_popup():
    root.popup = NetworkPopup(root)
    root.update_idletasks()


def close_popup():
    root.popup.destroy()


class GenericInputPopup(tk.Toplevel, ABC):
    """input window requires a master"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.geometry("360x150+480+500")
        self.title("Input")

        self.lbl = tk.Label(self, font=("Segoe UI", 11))
        self.lbl.place(relx=0.5, rely=0.3, anchor="c")

        self.entry = tk.Entry(self, font=("Segoe UI", 11))
        self.entry.place(relx=0.5, rely=0.6, anchor="c")
        self.entry.bind("<Key-Return>", self.verify_entry)
        self.entry.bind("<KP_Enter>", self.verify_entry)
        self.entry.focus()

        self.lbl_entry_error = tk.Label(self, text="""Invalid""")
        self.lbl_entry_error.place(relx=0.5, rely=0.75, anchor="c")
        self.lbl_entry_error.configure(
            activebackground="#f9f9f9",
            activeforeground="black",
            # background="#d9d9d9",
            disabledforeground="#a3a3a3",
            font="-family {Segoe UI} -size 11 -weight bold",
            foreground="#ff0000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
        )

        self.lbl_entry_error_location = self.lbl_entry_error.place_info()
        self.hide_error()

        self.transient(master)
        self.grab_set()
        self.focus_force()

    def send_entry(self, data_info: str):
        data_bytes = self.get_input().encode()
        socket.send(data_bytes, data_info)

    @abstractmethod
    def verify_entry(self, _):
        """Function bound to <Enter> in entry.

        First hides error label by using hide_error().
        Shows error label if bad input by calling show_error() method

        Example:
        def verify_entry(self, _):
            self.hide_error()
            input = self.get_input()

            if (*bad input check*):
                self.show_error()
            else:
                *use input*
        """
        raise NotImplementedError

    def get_input(self):
        return self.entry.get().strip()

    def hide_error(self):
        self.lbl_entry_error.place_forget()

    def show_error(self):
        self.lbl_entry_error.place(
            relx=self.lbl_entry_error_location["relx"],
            rely=self.lbl_entry_error_location["rely"],
            anchor="c",
        )


class ShooterInputPopup(GenericInputPopup):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lbl.configure(text="Mata in namn, tex. (John Doe)")
        self.entry.bind("<Escape>", lambda e: close_input())

    def verify_entry(self, _):
        self.hide_error()
        input = self.get_input()

        if len(input) < 2:
            print("Ska ha minst två bokstäver", flush=True)
            self.show_error()
        else:
            self.send_entry("shooter")
            close_input()


class LeaderInputPopup(GenericInputPopup):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lbl.configure(text="Mata in skytte ledarens namn, tex. (L-O Nilsson)")

    def verify_entry(self, _):
        self.hide_error()
        input = self.get_input()

        if len(input) < 2:
            print("Ska ha minst två bokstäver", flush=True)
            self.show_error()
        else:
            global leader_name
            leader_name = self.entry.get()
            self.send_entry("leader")
            open_input(InputType.DATE)


class DateInputPopup(GenericInputPopup):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lbl.configure(text="Datum, (YYYY-MM-DD)")

    def verify_entry(self, _):
        self.hide_error()
        input = self.get_input()

        try:
            datetime.datetime.strptime(input, "%Y-%m-%d")
            print("This is the correct date string format.")
            self.send_entry("date")
            open_input(InputType.TIME)
        except ValueError:
            print(f"'{input}' is the incorrect date string format. It should be YYYY-MM-DD", flush=True)
            self.show_error()


class TimeInputPopup(GenericInputPopup):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.lbl.configure(text="Tid, (HH:MM)")

    def verify_entry(self, _):
        self.hide_error()
        input = self.get_input()

        try:
            datetime.datetime.strptime(input, "%H:%M")
            self.send_entry("time")
            close_input()
        except ValueError:
            print(f"'{input}' is the incorrect time string format. It should be HH:MM", flush=True)
            self.show_error()


class InputType(Enum):
    SHOOTER_NAME = auto()
    LEADER_NAME = auto()
    DATE = auto()
    TIME = auto()


def open_input(input_type: InputType):
    """input_type is an InputType Enum"""
    try:
        close_input()
    except (AttributeError, NameError):
        pass

    if not isinstance(input_type, InputType):
        raise TypeError("input_type must be an instance of InputType Enum")

    if input_type == InputType.SHOOTER_NAME:
        root.input = ShooterInputPopup(root)

    elif input_type == InputType.LEADER_NAME:
        root.input = LeaderInputPopup(root)

    elif input_type == InputType.DATE:
        root.input = DateInputPopup(root)

    elif input_type == InputType.TIME:
        root.input = TimeInputPopup(root)
    else:
        raise ValueError(f"Something went wrong, input type: {input_type} not matched")


def close_input():
    root.input.destroy()


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == "__main__":
    # First-Party
    import receiver

    receiver.vp_start_gui()