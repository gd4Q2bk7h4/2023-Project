import socket

def client():
    # 创建一个 socket 对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 服务器的 IP 地址和端口号
    host = '127.0.0.1'  # 或者服务器的实际IP地址
    port = 12345

    # 连接到服务器
    client_socket.connect((host, port))
    print("Connected to server")

    # 发送数据
    message = "Hello, server!"
    client_socket.send(message.encode('utf-8'))
    print("Message sent to server")

    # 接收响应
    response = client_socket.recv(1024)
    print("Received from server:", response.decode('utf-8'))

    # 关闭连接
    client_socket.close()

if __name__ == "__main__":
    client()
