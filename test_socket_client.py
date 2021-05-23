import socket
import pandas as pd
import pickle
from io import StringIO

HOST = '192.168.1.4'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Pre connection")
s.connect((HOST, PORT))
print("Connected")

while True:
    command = input("Enter your command: ")
    s.send(command.encode())

    if command == 'df':
        df = pickle.loads(s.recv(4096))
        print(df)
    elif command == 'df_csv':
        buffer = StringIO()
        s.recv_into(buffer)
        print(buffer.getvalue())
        df = pd.read_csv(pickle.loads(buffer))
        print(df)
    else:
        reply = s.recv(1024).decode()
        print(reply)

    if command == 'break':
        break