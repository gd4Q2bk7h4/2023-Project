import socket
import threading

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    try:
        while True:
            # 接收数据
            message = client_socket.recv(1024)
            if not message:
                break  # 客户端关闭连接
            print(f"Received message from {address}: {message.decode('utf-8')}")
            # 发送响应
            client_socket.send("Message received".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)  # 可以同时监听多个客户端，但这里设置了监听队列的大小
    print("Server listening on port 12345")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    server()
