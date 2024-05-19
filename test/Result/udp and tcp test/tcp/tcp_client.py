import socket

def tcp_client():
    server_address = ('localhost', 5000)
    message_count = 1000  # 发送100个数据包
    sent_count = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_address)
        for i in range(message_count):
            message = f'Packet {i}'.encode()
            sock.send(message)
            sent_count += 1
        print(f"Sent {sent_count} TCP packets.")

tcp_client()
