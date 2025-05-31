import threading
import sys
import socket

# Host & Port
host, port = sys.argv[1], int(sys.argv[2])
# IPV4 addr, TCP socket type
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Reuse address after waiting
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(5)

client_list = []  # list of connected users


# message thread for client upon connection
def client_thread(conn, addr):
    # sends message to connected client
    conn.send("Welcome to this room".encode('utf-8'))  # encoding strig into bytes

    while True:
        try:
            message = conn.recv(2048).decode('utf-8')  # decoding bytes into string
            if message:
                print("<" + addr[0] + "> " + message)
                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)

            else:
                # only break loop when sure the client has fully disconnected
                print(addr[0], "disconnected")
                remove(conn)
                break

        except:
            continue


# broadcast message to all clients whose object is not the same as the one sending the message
def broadcast(message, connection):
    for clients in client_list:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()

                remove(clients)  # if link is broken, remove client


def remove(connection):
    if connection in client_list:
        client_list.remove(connection)


while True:

    # accepts connection request and stores socket object/ IP address
    conn, addr = server.accept()

    # maintains list of clients
    client_list.append(conn)
    # prints the address of the user that just connected
    print(addr[0] + " connected")

    # creates and individual thread for every user that connects
    t = threading.Thread(target=client_thread, args=(conn, addr), daemon = True)
    t.start()