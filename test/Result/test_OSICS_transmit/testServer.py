import socket
import serial
import threading
import qontrol
import time

# TCP/IP settting
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

laserSerial = serial.Serial( # follow by user document of device
    port='COM8', #'/dev/ttyUSB0'
    baudrate=9600,         
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    timeout=0.5                
)
#PM32 = qontrol.SXInput(serial_port_name='/dev/ttyUSB1')
#PM32.get_value(0, 'I')

def lasertransmit(command_string,ser,socket):# to send command to serial device
    if not ser.is_open:
        ser.open()
    ser.write(command_string)
    print(command_string)
    outputData = ser.readline()
    outputData  = outputData.decode('utf-8').strip()
    outputData = outputData.replace('\r>', '')
    outputData = str(outputData)
    print(outputData)
    outputData = outputData.encode('utf-8')
    try:
        socket.send(outputData)
    except ConnectionResetError:
        socket.close()
    

def handle_client_connection(client_socket):
    while True:
        # data from PC
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        
        data = data.decode('utf-8')
        print(data)
        if data.lower() == 'quit':
            print("program end")
            break
        elif(data.lower() == 'help'):
            print("Help Information:")
        elif(data.startswith('OSICS')):
            command = (data[5:] + '\r').encode('ascii')
            lasertransmit(command,laserSerial,client_socket)
        elif(data.startswith('2')):
            command = ''
    client_socket.close()

# create socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

print("wait PC connecting...")

# 
while True:
    conn, addr = s.accept()
    print('connection IP address：', addr)
    client_thread = threading.Thread(target=handle_client_connection, args=(conn,))
    client_thread.start()
