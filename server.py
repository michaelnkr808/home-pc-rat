import socket

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s.socket.socket()
    except socket.error as msg:
        print("Socket Creation Error " + str(msg))

# Binding socket and listening for connections

def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port " + str(port))

        s.bind((host, port))
        s.listen(5)
        
    except socket.error as msg:
        print("Socket Binding Error " + str(msg) + "\n" "Retrying...")
        bind_socket()

# Establish fection with client and socket must be listening

def socket_accept():
    conn, address = s.accept
    print("Connection has been established | " + "ip" + address[0] + " | Port" + str(address[1]))
    send_command(conn)
    conn.close
