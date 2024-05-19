import socket
import time

def tcp_throughput_test(duration=10):
    message = b'Test Message' # 1KB of data to send
    i = 0
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    start_time = time.time()
    end_time = start_time + duration
    bytes_transferred = 0
    while time.time() < end_time:
        i += 1
        client_socket.send(message)
        bytes_transferred += len(message)
    print(f"TCP Throughput: {bytes_transferred / (time.time() - start_time)} bytes/sec")
    print(i)

if __name__ == "__main__":
    tcp_throughput_test()
