import socket
import threading

HOST = "0.0.0.0"
PORT = 9999
END_MARKER = "<END_OF_OUTPUT>"

def recv_loop(conn):
    buf = ""
    while True:
        try:
            chunk = conn.recv(4096)
        except OSError:
            print("\nReciever socket closed")
            break
        if not chunk:
            print("\nClient Disconnected")
            break
        buf += chunk.decode()
        while END_MARKER in buf:
            out, buf = buf.split(END_MARKER, 1)
            if out:
                print(f"\n{out}", end="")
            print("Enter a command: ", end="", flush=True)

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

conn, addr = server.accept()
print(f"Connected to client: {addr}")
threading.Thread(target=recv_loop, args=(conn,), daemon=True).start()
print("Enter a command: ", end ="", flush=True)


while True:
    cmd = input()
    if not cmd.strip():
        continue
    try:
        conn.send(cmd.encode())
    except (BrokenPipeError, OSError):
        print("Client disconnected, retrying...")
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            conn.close()
        except OSError:
            pass
        conn, addr = server.accept()
        print(f"Reconnected {addr}")
        threading.Thread(target = recv_loop, args=(conn,), daemon=True).start()

    