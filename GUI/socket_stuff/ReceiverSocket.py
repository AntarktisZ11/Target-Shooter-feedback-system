# Standard Library
from typing import Optional

# First-Party
import receiver_support
from BaseSocket import BaseSocket, Tk, socket


class ReceiverSocket(BaseSocket):

    leader_name: Optional[str] = None
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, root: Tk, act_on_msg_func) -> None:
        super().__init__(root, act_on_msg_func)
        # self.connect()
        self.root.after(2000, self.connect)

    def connect(self):
        if self.ping_timer is not None:
            self.root.after_cancel(self.ping_timer)

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_support.open_popup()
        while True:
            try:
                self.conn.connect((self.HOST, self.PORT))
                self.conn.setblocking(0)
                break
            except (TimeoutError, ConnectionRefusedError, OSError) as e:
                print(e)
                if str(e) == "[Errno 106] Transport endpoint is already connected":
                    break
                print("Waiting to connect!")
                self.root.after(200)
                self.root.update()  # ! Allows accedental opening of input popup
        print("Connected")
        receiver_support.close_popup()
        if self.leader_name is None:
            self.root.after(
                300, receiver_support.open_input, receiver_support.InputType.LEADER_NAME
            )  # ! Don't forget to enable for print out
        else:
            self.send(self.leader_name.encode(), "leader")
        self.root.after(500)

        if self.recive_timer is not None:
            self.root.after_cancel(self.recive_timer)

        self.recive_timer = self.root.after(2000, self.recive)
        self.ping_timer = self.root.after(5000, self.ping)

    def reconnect(self):
        if not receiver_support.is_popup_open():
            self.connect()
