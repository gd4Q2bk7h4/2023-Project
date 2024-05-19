import socket

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(('localhost', 12346))
        print("UDP Server is waiting for data...")
        while True:
            data, addr = server_socket.recvfrom(1024)
            # 延迟测试：立即回复确认
            

if __name__ == "__main__":
    udp_server()
