import socket
import serial
import threading
from qontrol import SXInput
import ast
import datetime
import time

record_OSICS = 0
record_PM32_start = 0
OSICS_Laser_resourse = [True,True]
PM32_resource = [True]*16
lock_Laser = threading.Lock()

# TCP/IP settting
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

OSICS_Laser = serial.Serial( # follow by user document of device
    port='COM8', #'/dev/ttyUSB0'
    baudrate=9600,         
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    timeout=0.5                
)



def OSCII_Laser_transimit(serial,command_string):
    if not serial.is_open:
        serial.open()
    serial.write(command_string)
    try :
        while True:
            outputData = serial.readline()
            if outputData:
                outputData  = outputData.decode('utf-8').strip()
                outputData = outputData.replace('\r>', '')
                break
    except KeyboardInterrupt:
        print("program end")
    serial.close()
    return outputData

def response_To_PC(socket,respose):
    respose = str(respose)
    print(respose)
    respose = respose.encode('utf-8')
    data_size = len(respose)
    header=bytes(str(data_size),'utf-8').zfill(8)
    try:
        socket.send(header)
        socket.send(respose)
    except ConnectionResetError:
        socket.close()

def check_value_in_list(index_list,check_list):
    for index in index_list:
        if index >= len(index_list):
            return False
        
        if not check_list[index]:
            return False
    return False

def handle_client_connection(client_socket):
    while True:
        # data from PC
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            break
        request = request.decode('utf-8')
        print(request)
        if(request.startswith('OSICS')):
            command = request.replace('OSICS','')
            with lock_Laser:
                print(datetime.datetime.now())
                if command.startswith('channellock:'):
                    lock_channel = int(command.split(':')[1])
                    if OSICS_Laser_resourse[lock_channel-1] == True:
                        OSICS_Laser_resourse[lock_channel-1] == False
                        response_To_PC(client_socket,'The channel has been lock')
                    else:
                        available_Laser = [str(index + 1) for index, value in enumerate(OSICS_Laser_resourse) if not value]
                        response = f'Error,The avaiable laser channel is {available_Laser}'
                        response_To_PC(socket,response)
                        break
                elif command.startswith('channellock:'):
                    release_channel = int(command.split(':')[1])
                    OSICS_Laser_resourse[release_channel-1] == True
                    response_To_PC(client_socket,'The channel has been release')     
                else:
                    to_laser_command = (command + '\r').encode('ascii')
                    laser_reuslt = OSCII_Laser_transimit(serial=OSICS_Laser,command_string=to_laser_command)
                    response_To_PC(client_socket,laser_reuslt)
    client_socket.close()

def server_main():
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

if __name__ == '__main__':
    server_main()