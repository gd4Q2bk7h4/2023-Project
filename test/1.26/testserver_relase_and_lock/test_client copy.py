import socket
import datetime
import time

def start_client():
    host = "127.0.0.1"
    port = 5005

    clientSocket = socket.socket()
    clientSocket.connect((host, port))
    for i in range(5):
        clientSocket.send(b'heartbeat')
        print(datetime.datetime.now())
        time.sleep(1)
            # send heartbeat every 10 seconds

start_client()
