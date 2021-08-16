# Standard modules
from typing import Optional

# Local files
from .BaseSocket import BaseSocket, socket, select, Tk, SELECT_FUNC_TIMEOUT
import sender_extra_windows as windows

MAX_ATTEMPTS = 50
ROOT_UPDATE_RATE = 10  # inverse relationship


class SenderSocket(BaseSocket):

    conn: Optional[socket.socket] = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, root: Tk, act_on_msg_func) -> None:
        super().__init__(root, act_on_msg_func)

        i = 1
        while i <= MAX_ATTEMPTS:  # True would work as well
            try:
                self.s.bind((self.HOST, self.PORT))
                print("Bound succesfully")
                break
            except socket.error:
                print(f"Bind {i} failed")
                root.after(500)
                if i == MAX_ATTEMPTS:
                    print(f"Closing...\nCheck host address, currently {self.HOST}")
                    root.destroy()
            i += 1

        self.listen()

    def listen(self):
        print("Starting listen")
        if self.ping_timer is not None:
            print(f"Canceling {self.ping_timer}")
            self.root.after_cancel(self.ping_timer)

        if self.conn is not None:
            print(f"Previously connected to {self.conn}")
            readable, writeable, e = select.select([self.conn], [self.conn], [self.conn], SELECT_FUNC_TIMEOUT)
            if readable:
                print("This was readable!")
            if writeable:
                print("This was writeable!")
            if e:
                print("This was e!")
            if writeable and (not readable):
                print("Should skip this as it is alreday connected!")
                return

        self.s.listen(1)
        self.s.setblocking(False)
        print("Socket awaitning connection")
        i = 0
        windows.open_network_popup()
        while True:
            try:
                (self.conn, addr) = self.s.accept()
                break
            except BlockingIOError:
                i += 1
                print(r"/-\|"[i % 4] + "\r", end="", flush=True)
                if i % ROOT_UPDATE_RATE == 0:
                    self.root.update()
        print("Connected")
        windows.close_network_popup()
        if self.recive_timer is not None:
            self.root.after_cancel(self.recive_timer)
        self.recive_timer = self.root.after(2000, self.recive)

    def reconnect(self):
        self.listen()
