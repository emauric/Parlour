import socket
import sys
import threading
import time

# Host & Port
host, port = sys.argv[1], int(sys.argv[2])
# IPV4 addr, TCP socket type
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((host, port))  # connect to server


# send messages via input
def write_sockets():
    while True:
        try:
            message = input("> ")
            server.send(message.encode('utf-8'))
        except Exception as e:
            print("Error Sending: ", e)
            continue


# receive messages via recv
def read_sockets():
    while True:
        try:
            message = server.recv(2048).decode('utf-8')
            if message:
                print(message)
        except Exception as e:
            print("Error Reading: ", e)
            continue


try:
    # Daemon threads will exit when the main program exits
    t1 = threading.Thread(target=read_sockets)
    t2 = threading.Thread(target=write_sockets)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
except KeyboardInterrupt:
    print("\nClient exiting...")
    time.sleep(5)
    server.close()
    sys.exit(0)
finally:
    print("Client disconnected.")
