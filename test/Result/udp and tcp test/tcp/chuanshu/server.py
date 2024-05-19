import socket

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 12345))
        server_socket.listen()
        print("TCP Server is waiting for connection...")
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                # 延迟测试：立即回复确认
                

if __name__ == "__main__":
    tcp_server()
