import socket
import time


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
command_string = "client2"
# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))

while True:
    s.send(command_string.encode())
    result = s.recv(1024)
    time.sleep(1)
    print(result)
