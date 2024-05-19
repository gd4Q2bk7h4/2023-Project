import socket
import time

def udp_throughput_test(duration=10):
    server_address = ('localhost', 12346)
    message = b'Test Message'  # 确保消息大小小于1472字节
    i = 0
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start_time = time.time()
    end_time = start_time + duration
    bytes_transferred = 0

    while time.time() < end_time:
        i += 1
        client_socket.sendto(message, server_address)
        # 假设回复大小与发送相同，接收确认
        bytes_transferred += len(message)

    throughput = bytes_transferred / duration
    print(f"UDP Throughput: {throughput} bytes/sec")
    print(i)

if __name__ == "__main__":
    udp_throughput_test()
