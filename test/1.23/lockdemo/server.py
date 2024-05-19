import socket
import threading
import time


# TCP/IP settting
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
lock1 = threading.Lock()
response = ""


def handle_client_connection(client_socket):
    
        while True:
            request = client_socket.recv(BUFFER_SIZE)
            if not request:
                break
            request = request.decode('utf-8')
            if request.startswith("client"):
                with lock1:
                    if request == "client1" :
                        response = 'hello world! to client1'
                        response = response.encode('utf-8')
                    else:
                        response = 'hello world! to client2'
                        response = response.encode('utf-8')
                    print(request)
                client_socket.send(response)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

print("wait PC connecting...")

# 
while True:
    conn, addr = s.accept()
    print('connection IP address：', addr)
    client_thread = threading.Thread(target=handle_client_connection, args=(conn,))
    client_thread.start()