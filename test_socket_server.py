import time
import socket
import pandas as pd
import pickle
from io import StringIO
import select

HOST = '192.168.1.4'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed')


df = pd.DataFrame([[0,1,2], [1,2,3], [2,3,4]])
print(df)
df_bytes = pickle.dumps(df)
print(df_bytes.__sizeof__())

def listen():
    s.listen(1)
    s.setblocking(False)
    print("Socket awaitning connection")
    global conn, addr
    i=0
    while True:
        try:
            (conn, addr) = s.accept()
            break
        except BlockingIOError:
            i += 1
            print('/-\|'[i%4]+'\r',end='',flush=True)
    print("Connected")


def reply(data, data_info):
    data_info = data_info.lower()
    if len(str(data_info)) != 8:
        raise ValueError("Data_info has to be 8 characters, was: " + str(len(data_info)))
    size = len(data) + len(data_info) + 2   # 2 is for "packet_len"
    MAX_BYTE = int(0xFF)
    packet_len = bytes([size//MAX_BYTE, size % MAX_BYTE]) # Returns two bytes to store the packet size excluding bytes for TCP protocoll
    prefix = packet_len + data_info.encode()
    print(len(data + prefix))
    try:
        conn.sendall(prefix + data)
    except (ConnectionResetError, ConnectionAbortedError) as e:
        print(e)
        listen()
        reply(data, data_info)


def main():
    i=0
    listen()
    while True:
        r,w,e = select.select([conn], [], [], 0.2)
        if r:
            try:
                msg = conn.recv(1024).decode()
                print("I sent a message back in response to: " + msg)
            except (ConnectionResetError, ConnectionAbortedError) as e:
                print(e)
                main()
            

            if msg == 'break':
                reply("Breaking connection".encode(), "Breaking")
                print("Breaking connection")
                time.sleep(2)
                conn.close()
                return
            elif msg == 'df':
                reply(df_bytes, "DataFram")
                reply(df_bytes, "DataFram")
            elif msg == 'df_csv':
                buffer = StringIO() # Behaves as a txt file but in memory
                df.to_csv(buffer)
                reply(pickle.dumps(buffer), "df_csv  ")
            else:
                reply("Hello, world!".encode(), "Greeting")

        i += 1
        print('/-\|'[i%4]+'\r',end='',flush=True)

if __name__ == '__main__':
    main()