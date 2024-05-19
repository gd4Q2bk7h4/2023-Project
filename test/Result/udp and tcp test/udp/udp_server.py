import socket

def udp_server():
    host = 'localhost'
    port = 5001
    received_count = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((host, port))
        print("UDP Server listening...")
        while True:
            data, addr = sock.recvfrom(1024)
            if data:
                received_count += 1
                print(f"Received packet: {data.decode()}")
             
            if received_count == 1000:
                break

    print(f"Received {received_count} UDP packets.")

udp_server()
