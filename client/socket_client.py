import socket
import sys
import threading

# Host & Port
host, port = sys.argv[1], int(sys.argv[2])
# IPV4 addr, TCP socket type
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(host, port)  # connect to server


# send messages via input
def write_sockets():
    while True:
        try:
            message = input("> ")
            server.send(message.encode('utf-8'))
        except:
            print("An error occurred while sending.")
            server.close()
            break


# receive messages via recv
def read_sockets():
    while True:
        try:
            message = server.recv(2048).decode('utf-8')
            print(message)
        except:
            print("An error occurred while reading.")
            server.close()
            break


# Daemon threads will exit when the main program exits
t1 = threading.Thread(target=read_sockets, daemon=True).start()
t2 = threading.Thread(target=write_sockets, daemon=True).start()
