#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 6.1
#  in conjunction with Tcl version 8.6
#    May 19, 2021 10:15:54 PM CEST  platform: Windows NT

# ! Made for python 3.7 and 3.8

# Standard Library
import sys
import tkinter as tk
import tkinter.font as Tkfont
import tkinter.ttk as ttk

# First-Party
import sender_extra_windows as windows
import sender_support


def vp_start_gui():
    """Starting point when module is the main routine."""
    global val, w, root
    root = tk.Tk()
    sender_support.set_Tk_var()
    top = Toplevel1(root)
    sender_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    """Starting point when module is imported by another module.
    Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' ."""
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    sender_support.set_Tk_var()
    top = Toplevel1(w)
    sender_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
        Top is the toplevel containing window."""
        _bgcolor = "#d9d9d9"  # X11 color: 'gray85'
        _fgcolor = "#000000"  # X11 color: 'black'
        _compcolor = "#d9d9d9"  # X11 color: 'gray85'
        # _ana1color = "#d9d9d9"  # X11 color: 'gray85'
        _ana2color = "#ececec"  # Closest X11 color: 'gray92'
        default_font = Tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=13)

        root.option_add("*Font", default_font)
        self.style = ttk.Style()
        self.style.configure(
            ".",
            background=_bgcolor,
            foreground=_fgcolor,
            font="TkDefaultFont",
        )
        self.style.map(
            ".",
            background=[
                ("selected", _compcolor),
                ("active", _ana2color),
            ],
        )

        self.style.configure(
            "TCombobox",
            selectbackground="white",
            selectforeground="black",
            padding=3,
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[
                ("readonly", "white"),
                ("disabled", _bgcolor),
            ],
        )

        top.geometry("800x450")
        top.minsize(120, 1)
        top.maxsize(1920, 1080)
        top.resizable(0, 0)
        if sys.platform == "linux":
            top.attributes("-fullscreen", True)
        top.title("Träffmarkerare")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        """
            -------  Image  ---------
        """

        self.Frame_Image = tk.Frame(top)
        self.Frame_Image.place(x=270, y=0, height=450, width=530)
        self.Frame_Image.configure(background="#d9d9d9")

        self.Image = tk.Label(self.Frame_Image)
        self.Image.place(relx=0.5, rely=0.5, anchor="c")
        self.Image.configure(
            background="#d9d9d9",
            text="""Bild""",
        )

        """
            -------  Name-combobox  ---------
        """

        self.Label_name = tk.Label(top, text="""Namn: """)
        self.Label_name.place(x=10, y=20, height=23, width=70)
        self.Label_name.configure(
            background="#d9d9d9",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            takefocus="",
            justify="right",
        )

        self.TCombobox1 = ttk.Combobox(top)
        self.TCombobox1.place(x=80, y=20, height=28, width=150)
        self.TCombobox1.configure(
            state="readonly",
            takefocus="0",
        )
        self.TCombobox1.bind("<FocusIn>", sender_support._from_combobox)
        self.TCombobox1.bind("<Button-3>", self.popup1)

        self.tooltip_font = "TkDefaultFont"
        self.Combobox_tooltip = ToolTip(self.TCombobox1, self.tooltip_font, "")
        self.Combobox_tooltip.disable()

        """
            -------  Radiobuttons  ---------
        """

        self.Frame_radio = tk.Frame(top)
        self.Frame_radio.place(x=10, y=60, height=55, width=230)
        self.Frame_radio.configure(background="#d9d9d9")
        self.Frame_radio.grid_columnconfigure(0, weight=1)
        self.Frame_radio.grid_columnconfigure(1, weight=1)

        self.Radiobutton1 = tk.Radiobutton(self.Frame_radio, value=1, text="""Stilla""")
        self.Radiobutton2 = tk.Radiobutton(self.Frame_radio, value=2, text="""Jaktskott""")
        self.Radiobutton3 = tk.Radiobutton(self.Frame_radio, value=3, text="""Löpande""")
        self.Radiobutton4 = tk.Radiobutton(self.Frame_radio, value=4, text="""Dubble""")

        # self.tooltip_font = "TkDefaultFont"
        # self.Radiobutton1_tooltip = \
        # ToolTip(self.Radiobutton1, self.tooltip_font, '''Stillastående''')

        self.Radiobutton1.grid(row=0, column=0, sticky="W")
        self.Radiobutton2.grid(row=1, column=0, sticky="W")
        self.Radiobutton3.grid(row=0, column=1, sticky="W")
        self.Radiobutton4.grid(row=1, column=1, sticky="W")

        self.radiobuttons = [
            self.Radiobutton1,
            self.Radiobutton2,
            self.Radiobutton3,
            self.Radiobutton4,
        ]

        for rb in self.radiobuttons:
            rb.configure(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                command=sender_support.allow_entry,
                disabledforeground="#a3a3a3",
                foreground="#000000",
                highlightbackground="#d9d9d9",
                highlightcolor="black",
                justify="left",
                takefocus="0",
                variable=sender_support.selectedButton,
            )

        """
            -------  Entry  ---------
        """

        self.Frame_entry = tk.Frame(top)
        self.Frame_entry.place(x=30, y=140, height=90, width=200)
        self.Frame_entry.configure(background="#d9d9d9")
        self.Frame_entry.grid_columnconfigure(0, weight=1)
        self.Frame_entry.grid_columnconfigure(1, weight=1)

        self.Entry_Point = tk.Entry(self.Frame_entry)
        self.Entry_Point.bind("<Key-Return>", sender_support.point_entry)
        self.Entry_Point.bind("<KP_Enter>", sender_support.point_entry)

        self.Entry_Clock = tk.Entry(self.Frame_entry)
        self.Entry_Clock.bind("<Key-Return>", sender_support.clock_entry)
        self.Entry_Clock.bind("<KP_Enter>", sender_support.clock_entry)

        self.Entry_Point.grid(row=1, column=0, padx=20, sticky="")
        self.Entry_Clock.grid(row=1, column=1, padx=20, sticky="")

        self.entries = [
            self.Entry_Point,
            self.Entry_Clock,
        ]

        for entry in self.entries:
            entry.configure(
                background="white",
                disabledforeground="#a3a3a3",
                foreground="#000000",
                highlightbackground="#d9d9d9",
                highlightcolor="black",
                insertbackground="black",
                justify="center",
                selectbackground="blue",
                selectforeground="white",
            )

        self.Label_point = tk.Label(self.Frame_entry, text="""Poäng""", background="#d9d9d9")
        self.Label_clock = tk.Label(self.Frame_entry, text="""Klocka""", background="#d9d9d9")

        self.Label_point.grid(row=0, column=0, pady=2, sticky="N")
        self.Label_clock.grid(row=0, column=1, pady=2, sticky="N")

        self.Label_PointError = tk.Label(self.Frame_entry)
        self.Label_ClockError = tk.Label(self.Frame_entry)

        self.Label_PointError.grid(row=2, column=0, sticky="N")
        self.Label_ClockError.grid(row=2, column=1, sticky="N")

        self.error_lbls = [
            self.Label_PointError,
            self.Label_ClockError,
        ]

        for lbl in self.error_lbls:
            lbl.configure(
                background="#d9d9d9",
                font="-family {Segoe UI} -size 9 -weight bold",
                foreground="#ff0000",
                text="""Invalid""",
            )

        """
            -------  Log  ---------
        """

        self.Listbox1 = tk.Listbox(top)
        self.Listbox1.place(x=30, y=230, height=150, width=200)
        self.Listbox1.configure(
            background="white",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            selectbackground="blue",
            selectforeground="white",
            takefocus="0",
        )
        self.Listbox1.bind("<Key-Delete>", sender_support.delete_item)
        self.Listbox1.bind("<Key-BackSpace>", sender_support.delete_item)

        """
            -------  Buttons  ---------
        """

        self.Exit = tk.Button(top)
        self.Exit.place(x=40, y=400, height=30, width=50)
        self.Exit.configure(activebackground="#ececec")
        self.Exit.configure(activeforeground="#000000")
        self.Exit.configure(background="#d9d9d9")
        self.Exit.configure(command=windows.open_exit_popup)
        self.Exit.configure(disabledforeground="#a3a3a3")
        self.Exit.configure(foreground="#000000")
        self.Exit.configure(highlightbackground="#d9d9d9")
        self.Exit.configure(highlightcolor="black")
        self.Exit.configure(pady="0")
        self.Exit.configure(text="""Exit""")

        self.Button_Undo = tk.Button(top)
        self.Button_Undo.place(x=140, y=400, height=30, width=80)
        self.Button_Undo.configure(activebackground="#ececec")
        self.Button_Undo.configure(activeforeground="#000000")
        self.Button_Undo.configure(background="#d9d9d9")
        self.Button_Undo.configure(command=lambda: sender_support.delete_item("doesNothing", latest=True))
        self.Button_Undo.configure(disabledforeground="#a3a3a3")
        self.Button_Undo.configure(foreground="#000000")
        self.Button_Undo.configure(highlightbackground="#d9d9d9")
        self.Button_Undo.configure(highlightcolor="black")
        self.Button_Undo.configure(pady="0")
        self.Button_Undo.configure(text="""Ångra""")

        """
            -------  Menubar  ---------
        """

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.sub_menu = tk.Menu(
            top,
            activebackground="#ececec",
            activeborderwidth=1,
            activeforeground="#000000",
            background="#d9d9d9",
            borderwidth=1,
            disabledforeground="#a3a3a3",
            foreground="#000000",
            tearoff=0,
        )
        self.menubar.add_cascade(menu=self.sub_menu, label="Inställningar")
        self.sub_menu.add_checkbutton(
            variable=sender_support.free_mode_check,
            command=sender_support.free_mode,
            label="Fritt läge [Experimentell]",
        )
        self.menubar.add_command(command=windows.open_print_window, label="Skriv ut")
        self.menubar.add_command(command=windows.open_point_window, label="Träff tabell")
        self.menubar.add_command(command=windows.open_help, label="Hjälp")

    # @staticmethod
    def popup1(self, event, *args, **kwargs):
        Popupmenu1 = tk.Menu(root, tearoff=0)
        Popupmenu1.configure(activebackground="#ececec")
        Popupmenu1.configure(activeborderwidth="1")
        Popupmenu1.configure(activeforeground="#000000")
        Popupmenu1.configure(background="#d9d9d9")
        Popupmenu1.configure(borderwidth="1")
        Popupmenu1.configure(disabledforeground="#a3a3a3")
        Popupmenu1.configure(foreground="#000000")

        if self.TCombobox1.get() != "":
            Popupmenu1.add_command(label="Delete user", command=sender_support.delete_user)
        Popupmenu1.post(event.x_root, event.y_root)

    @staticmethod
    def popup2(event, *args, **kwargs):
        Popupmenu2 = tk.Menu(root, tearoff=0)
        Popupmenu2.configure(activebackground="#ececec")
        Popupmenu2.configure(activeborderwidth="1")
        Popupmenu2.configure(activeforeground="#000000")
        Popupmenu2.configure(background="#d9d9d9")
        Popupmenu2.configure(borderwidth="1")
        Popupmenu2.configure(disabledforeground="#a3a3a3")
        Popupmenu2.configure(foreground="#000000")
        Popupmenu2.post(event.x_root, event.y_root)

    @staticmethod
    def popup3(event, *args, **kwargs):
        Popupmenu3 = tk.Menu(root, tearoff=0)
        Popupmenu3.configure(activebackground="#ececec")
        Popupmenu3.configure(activeborderwidth="1")
        Popupmenu3.configure(activeforeground="#000000")
        Popupmenu3.configure(background="#d9d9d9")
        Popupmenu3.configure(borderwidth="1")
        Popupmenu3.configure(disabledforeground="#a3a3a3")
        Popupmenu3.configure(foreground="#000000")
        Popupmenu3.post(event.x_root, event.y_root)


# ======================================================
# Support code for Balloon Help (also called tooltips).
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# Modified by Antarktis to add enabling/disabling of tooltip
# ======================================================

# Standard Library
from time import time


class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """

    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None, delay=0.5, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg="black", padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set("No message provided")
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(
            self,
            textvariable=self.msgVar,
            bg="#FFFFDD",
            font=tooltip_font,
            aspect=1000,
        ).grid()

        self.is_enabled = False
        self.enable()

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in milliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.

        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry("+%i+%i" % (event.x_root + 20, event.y_root - 10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except Exception:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget

        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        """
        Updates the Tooltip with a new message. Added by Rozen
        """
        self.msgVar.set(msg)

    def enable(self):
        """
        Enables the Tooltip by rebinding. Added by Antarktis

        Adds bindings to the widget. This will NOT override
        bindings that the widget already has!
        """
        if not self.is_enabled:
            self.bind_id_spawn = self.wdgt.bind("<Enter>", self.spawn, "+")
            self.bind_id_hide = self.wdgt.bind("<Leave>", self.hide, "+")
            self.bind_id_move = self.wdgt.bind("<Motion>", self.move, "+")
            self.is_enabled = True

    def disable(self):
        """
        Disables the Tooltip by unbinding. Added by Antarktis
        """
        if self.is_enabled:
            self.wdgt.unbind("<Enter>", self.bind_id_spawn)
            self.wdgt.unbind("<Leave>", self.bind_id_hide)
            self.wdgt.unbind("<Motion>", self.bind_id_move)
            self.is_enabled = False


# ===========================================================
#                   End of Class ToolTip
# ===========================================================

if __name__ == "__main__":
    vp_start_gui()