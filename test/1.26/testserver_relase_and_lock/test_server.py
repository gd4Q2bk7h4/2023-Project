# import socket
# import threading
# import time
# import datetime

# class ClientThread(threading.Thread):
#     no_command_time = 0
#     def __init__(self, clientAddress, clientSocket):
#         threading.Thread.__init__(self)
#         self.clientSocket = clientSocket
#         print(f"[+] New connection from {clientAddress}")
#         print(f'connected: {datetime.datetime.now()}')

#     def run(self):
#         while True:
#             try:
#                 message = self.clientSocket.recv(1024)
#                 if not message:
#                     no_command_time = datetime.datetime.now()
#                     if (datetime.datetime.now() - no_command_time).total_seconds() == 10:
#                             print('time out')
#                             self.clientSocket.close()
#                     else:
#                         break
#             except:
#                 break

#         self.clientSocket.close()

# def start_server():
#     host = "127.0.0.1"
#     port = 12345
#     serverSocket = socket.socket()
#     serverSocket.bind((host, port))
#     print("Server started")
#     print("Waiting for clients...")

#     while True:
#         serverSocket.listen(5)
#         clientSock, clientAddress = serverSocket.accept()
#         newThread = ClientThread(clientAddress, clientSock)
#         newThread.start()

# start_server()

# import socket
# import threading
# import time

# # 资源锁定状态表
# resource_locks = {'channel1': None, 'channel2': None}

# # 处理客户端请求的函数
# def handle_client(client_socket):
#     while True:
#         # 接收客户端消息
#         message = client_socket.recv(1024).decode('utf-8')
        
#         if message.startswith("QUERY"):
#             # 查询资源状态
#             channel = message.split()[1]
#             if resource_locks[channel] is None:
#                 client_socket.send(b"Resource available")
#             else:
#                 client_socket.send(b"Resource locked")

#         elif message.startswith("LOCK"):
#             # 锁定资源
#             channel = message.split()[1]
#             if resource_locks[channel] is None:
#                 resource_locks[channel] = client_socket
#                 client_socket.send(b"Resource locked")
#             else:
#                 client_socket.send(b"Resource already locked")

#         elif message.startswith("UNLOCK"):
#             # 释放资源
#             channel = message.split()[1]
#             if resource_locks[channel] == client_socket:
#                 resource_locks[channel] = None
#                 client_socket.send(b"Resource unlocked")
#             else:
#                 client_socket.send(b"Invalid unlock attempt")

#         elif message == "EXIT":
#             break

#     client_socket.close()

# # 设置服务器
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('localhost', 12345))
# server_socket.listen(5)

# # 接受客户端连接
# while True:
#     client_sock, addr = server_socket.accept()
#     thread = threading.Thread(target=handle_client, args=(client_sock,))
#     thread.start()

import socket
import threading
import datetime

# TCP/IP settting
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

def ticker_opreation():
    print('time out')

def ticker_start():
    timer = threading.Timer(10,ticker_opreation).start()
    
def handle_client_connection(client_socket,addr):
    print(type(str(addr)))
    print(str(addr[0]))
    last_active_time = 0
    print(f'connect time: {datetime.datetime.now()}')
    while True:
        # data from PC
            request = client_socket.recv(BUFFER_SIZE)
            if not request:
                ticker_start()
                # while True:
                #     if (datetime.datetime.now() - last_active_time).total_seconds() >= 10:
                #         print(datetime.datetime.now())
                #         print('time out')
                #         break
                break
            request = request.decode('utf-8')
            last_active_time = datetime.datetime.now()
            print(request)
    client_socket.close()


def server_main():
    # create socket 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(2)
    

    print("wait PC connecting...")

    # 
    while True:
        conn, addr = s.accept()
        print('connection IP address：', addr)
        client_thread = threading.Thread(target=handle_client_connection, args=(conn,addr))
        client_thread.start()

if __name__ == '__main__':
    server_main()

