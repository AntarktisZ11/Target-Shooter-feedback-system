from abc import ABC, abstractmethod
import socket
import select

from tkinter import Tk
from typing import List, Tuple


MAX_INFO_LENGTH = 8  # characters
PACKET_LEN_VAR_SIZE = 2  # bytes
PACKET_PREFIX_SIZE = PACKET_LEN_VAR_SIZE + MAX_INFO_LENGTH
FULL_BYTE = int(0xFF)
SELECT_FUNC_TIMEOUT = 0.2  # seconds
RECV_BUFFER_SIZE = 2048  # bytes


class BaseSocket(ABC):

    conn: socket.socket
    msg_list: List[Tuple[bytes, str]] = []
    HOST = "192.168.1.90"
    PORT = 12345
    ping_timer, recive_timer = None, None

    def __init__(self, root: Tk, act_on_msg_func) -> None:
        self.root = root
        self.act_on_msg = act_on_msg_func

    @abstractmethod
    def reconnect(self):
        """Override in subclass.
        Implement how the socket will try to reconnect"""
        pass

    # @abstractmethod
    # def act_on_msg(self):
    #     """Override in subclass.
    #     Implement how the received data will be utilized"""
    #     pass

    def send(self, data: bytes, data_info: str):
        data_info = data_info.lower()
        if len(str(data_info)) > MAX_INFO_LENGTH:
            raise ValueError(f"Data_info has to be max {MAX_INFO_LENGTH} characters, was: {len(data_info)}")
        data_info = f"{data_info:<{MAX_INFO_LENGTH}}"

        size = len(data) + len(data_info) + PACKET_LEN_VAR_SIZE
        packet_len = bytes(
            [size // FULL_BYTE, size % FULL_BYTE]
        )  # Returns two bytes to store the packet size excluding size of TCP protocoll
        prefix = packet_len + data_info.encode()
        print(len(prefix + data))
        try:
            self.conn.sendall(prefix + data)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
            print(e)
            self.reconnect()
            self.send(data, data_info)

    def recive(self):
        # print("Reciveing")
        msg = b""
        list = []
        length = 0
        has_read = False
        while True:
            r, w, _ = select.select([self.conn], [], [], SELECT_FUNC_TIMEOUT)
            if r:
                try:
                    msg += self.conn.recv(RECV_BUFFER_SIZE)
                    has_read = True
                except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError) as e:
                    print(e)
                    self.reconnect()

            if len(msg) >= PACKET_LEN_VAR_SIZE:

                if length == 0:
                    length = int(msg[0]) * FULL_BYTE + int(msg[1])  # Convert first PACKET_LEN_VAR_SIZE bytes to decimal
                    print(length)

                if len(msg) >= length and length:
                    data_info = msg[PACKET_LEN_VAR_SIZE:PACKET_PREFIX_SIZE]
                    data = msg[PACKET_PREFIX_SIZE:length]
                    list.append((data, data_info.decode().strip()))
                    msg = msg[length:]
                    length = 0

            if not len(msg):
                self.recive_timer = self.root.after(500, self.recive)
                if has_read:
                    self.msg_list.extend(list)
                    self.root.after(0, self.act_on_msg)
                return

    def ping(self, periodic: bool = True):  # ! Maybe change periodic to auto_ping
        """Periodic makes the ping reschedule it self to ping every 5 seconds"""
        self.send(b"", "ping")
        if periodic:
            self.ping_timer = self.root.after(5000, self.ping)
