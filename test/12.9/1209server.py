import socket
import serial
import threading
import qontrol

# TCP/IP settting
TCP_IP = '192.168.137.48'
TCP_PORT = 5005
BUFFER_SIZE = 1024

laserSerial = serial.Serial( # follow by user document of device
    port='/dev/ttyUSB0', #'/dev/ttyUSB0'
    baudrate=9600,         
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    timeout=0.5                
)
PM32 = qontrol.SXInput(serial_port_name='/dev/ttyUSB1')
PM32.get_all_values('I')

def lasertransmit(command_string,ser):# to send command to serial device
    if not ser.is_open:
        ser.open
    ser.write(command_string)
    print(command_string)
    outputData = ser.readline()
    outputData  = outputData.decode('utf-8').strip()
    outputData = outputData.replace('\r>', '')
    return outputData

def response_To_PC(socket,respose):
    respose = str(respose)
    print(respose)
    respose = respose.encode('utf-8')
    try:
        socket.send(respose)
    except ConnectionResetError:
        socket.close()

def handle_client_connection(client_socket,lock):
    while True:
        # data from PC
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        data = data.decode('utf-8')
        print(data)

        if(data.startswith('OSICS')):
            with lock:
                to_laser_command = (data[5:] + '\r').encode('ascii')
                laser_reuslt = lasertransmit(to_laser_command,laserSerial)
                response_To_PC(laser_reuslt)
        elif(data.startswith('2')):
            with lock:
                measured_current = PM32.i[0]
                client_socket.send(measured_current)
        else:
            response_To_PC(client_socket,'Error Command')

    client_socket.close()

def main():
    #create lock to avoid race condition
    lock = threading.Lock()
    # create socket 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(2)

    print("wait PC connecting...")

    # 
    while True:
        conn, addr = s.accept()
        print('connection IP address：', addr)
        client_thread = threading.Thread(target=handle_client_connection, args=(conn,))
        client_thread.start()
