import socket
import pickle

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
        print(pickle.loads(s.recv(4096)))
    else:
        reply = s.recv(1024).decode()
        print(reply)

    if command == 'break':
        break