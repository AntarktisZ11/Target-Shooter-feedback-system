import socket
import pandas as pd
import pickle
import select
import time

HOST = '192.168.1.4'
PORT = 12345

print("Pre connection")
def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((HOST, PORT))
            s.setblocking(0)
            break
        except TimeoutError:
            print("Waiting to connect!")
    print("Connected")

def recive():
    MAX_BYTE = int(0xFF)
    msg = b''
    msg_list = []
    length = 0
    while True:
        r,w,e = select.select([s], [], [], 0.2)
        if r:
            try:
                msg += s.recv(2048)
            except (ConnectionResetError, ConnectionAbortedError) as e:
                print(e)
                connect()
            if len(msg) >= 2 and not length:
                length = int(msg[0])*MAX_BYTE + int(msg[1]) # Convert 2 bytes hex to decimal
                print(length)
            if len(msg) >= length and length:
                data_info = msg[2:10]
                data = msg[10:length]
                msg_list.append((data, data_info.decode()))
                msg = msg[length:]
                length = 0
        else:
            return msg_list


def main():
    connect()
    while True:
        command = input("Enter your command: ")
        try:
            s.send(command.encode())
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(e)
            print("Error: Lost connection - Reconnecting")
            command = None
            main()

        msg_list = recive()
        while msg_list:
            data, data_info = msg_list.pop(0)
            if data_info == "breaking":
                print("Server shuting down!")
                time.sleep(1)
                return
            elif data_info == "datafram":
                df = pickle.loads(data)
                print(df)
            elif data_info == "df_csv  ":
                unpickled_data = pickle.loads(data)
                unpickled_data.seek(0)
                df = pd.read_csv(unpickled_data, index_col=0)
                print(df)
            elif data_info == "greeting":
                print(data.decode())
            else:
                print("Unrecognizeable info: " + data_info)
                print("Was carrying this data: " + str(data))

if __name__ == '__main__':
    main()