import socket

HOST = '192.168.1.4'
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed')


s.listen(1)
print("Socket awaitning messages")
(conn, addr) = s.accept()
print("Connected")

while True:
    data = conn.recv(1024).decode()
    print("I sent a message back in response to: " + data)

    if data == 'break':
        conn.send("Breaking connection".encode())
        break
    else:
        reply = "Hello, world!"
        conn.send(reply.encode())
conn.close()