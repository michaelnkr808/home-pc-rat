import socket

HOST = "0.0.0.0"
PORT = 9999

server = socket.socket()
server.bind((HOST, PORT))
server.listen(5)

conn, addr = server.accept()
print("Connected ", addr)

while True:
    cmd = input("Enter a command: ")
    conn.send(cmd.encode())
    print(conn.recv(1024).decode)