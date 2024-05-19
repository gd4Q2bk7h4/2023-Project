import socket

def tcp_server():
    host = 'localhost'
    port = 5000
    received_count = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        print("TCP Server listening...")
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                received_count += 1
                print(f"Received packet: {data.decode()}")
            print(f"Received {received_count} TCP packets.")

tcp_server()
