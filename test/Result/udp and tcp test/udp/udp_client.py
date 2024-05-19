import socket

def udp_client():
    server_address = ('localhost', 5001)
    message_count = 1000  # send 1000 data packets
    sent_count = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for i in range(message_count):
            message = f'Packet {i}'.encode()
            sent = sock.sendto(message, server_address)
            if sent:
                sent_count += 1
        print(f"Sent {sent_count} UDP packets.")

udp_client()
