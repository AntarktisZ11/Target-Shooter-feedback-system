import sys
import os
import shutil

import pandas as pd
import numpy as np

import tkinter as tk
import tkinter.ttk as ttk


def init_globals(top, gui, program_location, user_list):
    global w, root, prog_location, users, leader_name
    w = gui
    root = top
    prog_location = program_location
    users = user_list
    # leader_name = leader_name_


def set_leader_name(name: str):
    global leader_name
    leader_name = name


"""
    -------  GenericPopup  ---------
"""


class GenericPopup(tk.Toplevel):
    """Window requires a master"""

    def __init__(self, master, width, height, title, **kwargs):
        super().__init__(master, **kwargs)
        self.geometry(f"{width}x{height}+{(800-width)//2}+{(480-height)//2}")  # set the position and size of the popup
        self.title(title)

        # The following commands keep the popup on top.
        # These commands must be at the end of __init__
        if sys.platform == "linux":
            self.wm_attributes("-type", "splash")  # remove border and titlebar #! Not tested
        self.transient(master)  # set to be on top of the main window
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)


"""
    -------  DistancePopup  ---------
"""


class DistancePopup(GenericPopup):
    def __init__(self, master):
        super().__init__(master, 320, 170, "Distance")

        lbl = tk.Label(self, text="Vilket avstånd är måltavlan på?", font=("Segoe UI", 11, "bold"))
        lbl.place(relx=0.5, rely=0.4, anchor="c")

        button_50 = tk.Button(self, text="50m", command=lambda: self.button_press("50m"))
        button_50.place(relx=0.3, rely=0.8, anchor="c")

        button_80 = tk.Button(self, text="80m", command=lambda: self.button_press("80m"))
        button_80.place(relx=0.7, rely=0.8, anchor="c")

    def button_press(self, selection):
        global distance
        distance = selection
        close_distance_popup()


def open_distance_popup():
    root.distance_popup = DistancePopup(root)
    root.update_idletasks()


def close_distance_popup():
    root.distance_popup.destroy()
    open_animal_popup()


"""
    -------  AnimalPopup  ---------
"""


class AnimalPopup(GenericPopup):
    def __init__(self, master):
        super().__init__(master, 320, 170, "Animal")

        lbl = tk.Label(self, text="Vilket djur?", font=("Segoe UI", 11, "bold"))
        lbl.place(relx=0.5, rely=0.4, anchor="c")

        button_moose = tk.Button(self, text="Älg", command=lambda: self.button_press("Älg"))
        button_moose.place(relx=0.3, rely=0.8, anchor="c")

        button_boar = tk.Button(self, text="Vildsvin", command=lambda: self.button_press("Vildsvin"))
        button_boar.place(relx=0.7, rely=0.8, anchor="c")

    def button_press(self, selection):
        global animal
        animal = selection
        close_animal_popup()


def open_animal_popup():
    root.animal_popup = AnimalPopup(root)
    root.update_idletasks()


def close_animal_popup():
    root.animal_popup.destroy()


"""
    -------  NetworkPopup  ---------
"""


class NetworkPopup(GenericPopup):
    def __init__(self, master):
        super().__init__(master, 320, 100, "Connecting...")

        lbl = tk.Label(self, text="Försöker koppla till skjutardatorn ... ", font=("Segoe UI", 11, "bold"))
        lbl.place(relx=0.5, rely=0.5, anchor="c")


def open_network_popup():
    root.network_popup = NetworkPopup(root)
    root.update_idletasks()


def close_network_popup():
    root.network_popup.destroy()


"""
    -------  PointWindow  ---------
"""


class PointWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Point Viewer")
        self.geometry("800x480")  # set the position and size of the window
        if sys.platform == "linux":
            self.attributes("-fullscreen", True)

        self.configure(background="#d9d9d9")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        """
            -------  Top  ---------
        """

        self.lbl_top = tk.Label(self, text="Välj användare")
        self.lbl_top.place(relx=0.5, rely=0.10, anchor="c")
        self.lbl_top.configure(
            background="#d9d9d9",
            font=("Segoe UI", 16),
        )

        self.combobox = ttk.Combobox(self, values=users)
        self.combobox.bind("<FocusIn>", lambda e: self.update_table())
        self.combobox.bind("<FocusIn>", lambda e: self.table_labels[0].focus(), add=True)
        self.combobox.set(w.TCombobox1.get())
        self.combobox.configure(
            state="readonly",
            takefocus="0",
        )

        self.combobox.place(relx=0.5, rely=0.2, anchor="c")

        """
            -------  Middle  ---------
        """

        self.table_container = tk.Frame(self, height=350, width=200, background="#d9d9d9")
        self.table_container.place(relx=0.5, rely=0.5, anchor="c")

        MAX_ROWS = 5
        MAX_COLUMNS = 4

        for i in range(MAX_ROWS):
            self.table_container.grid_rowconfigure(i, weight=1)

        for i in range(MAX_COLUMNS):
            self.table_container.grid_columnconfigure(i, weight=1)

        self.table_labels = []
        for n in range(MAX_ROWS * MAX_COLUMNS):
            self.table_labels.append(tk.Label(self.table_container))
            row = n // MAX_COLUMNS
            col = n % MAX_COLUMNS
            self.table_labels[n].grid(row=row, column=col, padx=10, sticky="NWSE")
            self.table_labels[n].configure(
                background="#d9d9d9",
                text=f" {row},{col} ",
                font=("Segoe UI", 18, "bold"),
            )

        """
            -------  Bottom  ---------
        """

        self.button_close = tk.Button(self, text="Tillbaka", command=self.destroy)
        self.button_close.place(relx=0.5, rely=0.85, anchor="c")

        """
            -------  Final  ---------
        """

        self.update_table()

        # The following commands keep the popup on top.
        # Remove these if you want a program with 2 responding windows.
        # These commands must be at the end of __init__
        self.transient(master)  # set to be on top of the main window
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)

    def update_table(self):
        user = self.combobox.get()
        if user == "":
            return
        user_df = self.format_dataframe(self.get_user_df(user))
        df_row_col_list = [user_df.columns.values]
        df_row_col_list.extend(user_df.values)
        i = 0
        for label in self.table_labels:
            row = i // 4
            col = i % 4
            label.configure(text=df_row_col_list[row][col])
            i += 1

    def format_dataframe(self, df: pd.DataFrame):
        df = df.fillna("-")
        for key in df.columns.values:
            df[key] = df[key].astype(str)
            df[key] = df[key].str.split(".")
            df[key] = df[key].str[0]
        return df

    def get_user_df(self, name: str):
        filename = os.path.join(prog_location, "csv", str(name) + ".csv")
        df = pd.read_csv(filename, squeeze=True)
        return df


def open_point_window():
    root.point_window = PointWindow(root)


def close_point_window():
    root.point_window.destroy()


"""
    -------  PrintWindow  ---------
"""


class PrintWindow(PointWindow):
    import pdflatex  # Local file
    import jinja2

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Print Window")

        env = self.pdflatex.JINJA2_ENV
        env["loader"] = self.jinja2.FileSystemLoader(prog_location)  # ! ( + subfolder)
        env = self.jinja2.Environment(**env)

        self.template = env.get_template("template.tex")

        """
            -------  Middle  ---------
        """

        try:
            # global leader_name
            self.leader_name = leader_name
        except NameError as e:
            print(e)
            self.leader_name = ""

        self.lbl_dist_n_animal = tk.Label(self)
        self.lbl_dist_n_animal.configure(
            text=f"{distance} {animal}",
            background="#d9d9d9",
            justify="left",
        )
        self.lbl_dist_n_animal.place(relx=0.8, rely=0.25, anchor="c")

        self.lbl_leader_name = tk.Label(self)
        self.lbl_leader_name.configure(
            text="Skjutledare: \n" + self.leader_name,
            background="#d9d9d9",
            justify="left",
        )
        self.lbl_leader_name.place(relx=0.8, rely=0.4, anchor="c")

        self.lbl_user_name = tk.Label(self)
        self.lbl_user_name.configure(
            text="Skytt: \n" + self.combobox.get(),
            background="#d9d9d9",
            justify="left",
        )
        self.lbl_user_name.place(relx=0.8, rely=0.6, anchor="c")
        self.combobox.bind("<FocusIn>", lambda e: self.update_user_name_lbl(), add=True)

        """
            -------  Bottom  ---------
        """

        self.button_print = tk.Button(self, text="Skriv ut", command=self.print_pdf)
        self.button_print.place(relx=0.7, rely=0.85, anchor="c")

        self.button_close.place_configure(relx=0.3)

    def update_user_name_lbl(self):
        self.lbl_user_name.configure(
            text="Skytt: \n" + self.combobox.get(),
        )

    def make_pdf(self):
        """Makes PDF of current user and returns full path to PDF"""
        user = self.combobox.get()
        if user == "":
            print("No user specified")
            return
        pdfl = self.pdflatex.PDFLaTeX.from_jinja2_template(
            self.template,
            user,
            distance=distance,  # Set from start modal window
            animal=animal,  # Set from start modal window
            data_frame_values=self.get_formated_df(user),
            leader_name=self.leader_name,
            shooter_name=self.format_name(user),
            date=r"\today\ \currenttime",
        )

        save_location = os.path.join(prog_location, "PDFs")
        pdf, log, cp = pdfl.create_pdf(keep_pdf_file=True, dir=save_location)
        print(cp, "\n\nPDF created!")
        pdf_fullpath = os.path.join(save_location, user + ".pdf")
        return pdf_fullpath

    def print_pdf(self):
        pdf_fullpath = self.make_pdf()
        if sys.platform == "linux":
            import cups

            conn = cups.Connection()
            printers = conn.getPrinters()
            printer_name = list(printers.keys())[0]
            conn.printFile(printer_name, pdf_fullpath, "", {})
        if sys.platform == "win32":
            os.startfile(pdf_fullpath, "open")
            # os.startfile(pdf_fullpath, "print") #! Not working for some reason: [WinError 1155]

    def get_formated_df(self, user: str):
        user_df = self.latex_format_dataframe(self.get_user_df(user))
        df_row_col_list = [user_df.columns.values]
        df_row_col_list.extend(user_df.values)
        df_col_row_list = np.array(df_row_col_list).T
        return df_col_row_list

    def latex_format_dataframe(self, df: pd.DataFrame):
        df = super().format_dataframe(df)
        for key in df.columns.values:
            df[key] = df[key].str.replace("51", "$5^{1}$")
        return df

    def format_name(self, user: str):
        return user.split(" [")[0]


def open_print_window():
    root.print_window = PrintWindow(root)


def close_print_window():
    root.print_window.destroy()


"""
    -------  HelpPopup  ---------
"""


class Help(GenericPopup):
    def __init__(self, master):
        super().__init__(master, 370, 270, "Help")

        self.help_texts = [
            """\
1. Välj ett namn i menyn till vänster
2. Välj ett av skyttestilarna
3. Mata in poäng (51, 5, 4, 3,
    T (= Träff i figur),
    0 (= Träff i figur),
    X (= Bom)
4. Mata in klockslag om möjligt (1-12)\
""",
            """\
Du kan öppna 'Träff tabell' för att se
träfftabellerna för varje skytt.\
""",
            """\
Du kan aktivera 'Fritt läge
[Experimentell]' under 'Inställnigar'.

Med den så är inmatningen inte
kopplad till någon skytt och man
kan mata in obegränsat.\
""",
        ]

        self.current_text_nr = 0

        self.lbl = tk.Label(self, text=self.help_texts[0], justify="left", font=("Segoe UI", 13))
        self.lbl.place(relx=0.5, rely=0.4, anchor="c")

        self.button_prev = tk.Button(self, text="Bakåt", command=self.prev_help)
        self.button_prev.place(relx=0.2, rely=0.85, anchor="c")

        self.button_close = tk.Button(self, text="Ok", command=close_help)
        self.button_close.place(relx=0.5, rely=0.85, anchor="c")

        self.button_next = tk.Button(self, text="Nästa", command=self.next_help)
        self.button_next.place(relx=0.8, rely=0.85, anchor="c")

    def next_help(self):
        total_help_texts = len(self.help_texts)
        self.current_text_nr = (self.current_text_nr + 1) % total_help_texts
        self.lbl["text"] = self.help_texts[self.current_text_nr]

    def prev_help(self):
        total_help_texts = len(self.help_texts)
        self.current_text_nr = (self.current_text_nr - 1) % total_help_texts
        self.lbl["text"] = self.help_texts[self.current_text_nr]


def open_help():
    root.help = Help(root)


def close_help():
    root.help.destroy()


"""
    -------  Exit verification popup  ---------
"""


class ExitPopup(GenericPopup):
    def __init__(self, master):
        super().__init__(master, 320, 170, "Exit")

        txt = """\
Avsluta program?

Kommer rensa skytte-data!\
"""

        lbl = tk.Label(self, text=txt, font=("Segoe UI", 11, "bold"))
        lbl.place(relx=0.5, rely=0.4, anchor="c")

        self.button_quit = tk.Button(self, text="Avsluta", command=self.exit)
        self.button_quit.place(relx=0.3, rely=0.85, anchor="c")

        self.button_cancel = tk.Button(self, text="Avbryt", command=close_exit_popup)
        self.button_cancel.place(relx=0.7, rely=0.85, anchor="c")

    def clear_folder(foldername):
        folder = os.path.join(prog_location, foldername)
        try:
            shutil.rmtree(folder)
            os.mkdir(folder)
        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")

    def exit(self):
        """Clean up and exit"""
        self.clear_folder("PDFs")
        self.clear_folder("csv")
        root.destroy()


def open_exit_popup():
    root.exit_popup = ExitPopup(root)


def close_exit_popup():
    root.exit_popup.destroy()
