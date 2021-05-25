import socket
import pandas as pd
import pickle

HOST = '192.168.1.4'
PORT = 12345

print("Pre connection")
def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((HOST, PORT))
            break
        except TimeoutError:
            print("Waiting to connect!")
    print("Connected")

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

        if command == 'df':
            df = pickle.loads(s.recv(4096))
            print(df)
        elif command == 'df_csv':
            pickled_data = s.recv(1024)
            unpickled_data = pickle.loads(pickled_data)
            unpickled_data.seek(0)
            df = pd.read_csv(unpickled_data,index_col=0)
            print(df)
        else:
            reply = s.recv(1024).decode()
            print(reply)

        if command == 'break':
            s.close()
            return

if __name__ == '__main__':
    main()