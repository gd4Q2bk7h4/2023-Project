import socket
import threading
TCP_IP = '10.168.207.210'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

def handle_client_connection(client_socket):
    while True:
        # data from PC
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        print(data)


while True:
    conn, addr = s.accept()
    print('connection IP address：', addr)
    client_thread = threading.Thread(target=handle_client_connection, args=(conn,))
    client_thread.start()