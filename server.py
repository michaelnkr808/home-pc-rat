import socket

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s.socket.socket()
    except:
        print("Socket Creation Error " str(msg))

#Binding socket and listening for connections

