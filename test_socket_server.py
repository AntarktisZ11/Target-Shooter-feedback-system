import socket
from numpy import diag_indices_from
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


s.listen(1)
print("Socket awaitning messages")
(conn, addr) = s.accept()
print("Connected")


while True:
    data = conn.recv(1024).decode()
    print("I sent a message back in response to: " + data)

    if data == 'break':
        conn.sendall("Breaking connection".encode())
        break
    elif data == 'df':
        conn.sendall(df_bytes)
    elif data == 'df_csv':
        buffer = StringIO()
        df.to_csv(buffer)
        conn.sendfile(buffer.getvalue())
    else:
        reply = "Hello, world!"
        conn.sendall(reply.encode())
conn.close()