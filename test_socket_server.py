import socket
import pandas as pd
import pickle
from io import StringIO

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
    print("Socket awaitning connection")
    global conn, addr
    (conn, addr) = s.accept()
    print("Connected")

def main():
    listen()
    while True:
        try:
            data = conn.recv(1024).decode()
            print("I sent a message back in response to: " + data)
        except ConnectionResetError as e:
            print(e)
            main()

        if data == 'break':
            conn.sendall("Breaking connection".encode())
            print("Breaking connection")
            conn.close()
            break
        elif data == 'df':
            conn.sendall(df_bytes)
        elif data == 'df_csv':
            buffer = StringIO() # Behaves as a txt file but in memory
            df.to_csv(buffer)
            df_pickled = pickle.dumps(buffer)
            print(df_pickled.__sizeof__())
            conn.sendall(df_pickled)
        else:
            reply = "Hello, world!"
            conn.sendall(reply.encode())
    

if __name__ == '__main__':
    main()