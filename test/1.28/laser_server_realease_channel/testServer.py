import socket
import serial
import threading
from qontrol import SXInput

OSICS_Laser_resourse = {f'CH{i}': None for i in range(1, 3)}
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

def check_laser_channel(channel_number):
    global OSICS_Laser_resourse
    channel_key = f'CH{channel_number}'
    if OSICS_Laser_resourse[channel_key] is None:
        OSICS_Laser_resourse[channel_key] = 'using'
        return True
    else:
        return False

def release_laser_channel(channel_number):
    global OSICS_Laser_resourse
    if not OSICS_Laser_resourse[channel_number] is None:
        OSICS_Laser_resourse[channel_number] = None

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

def ticker_opreation(channel_number):
    print('time out')
    release_laser_channel(channel_number)
    print('The device resources has release')

def ticker_start(channel_number):
    timer = threading.Timer(20,lambda: ticker_opreation(channel_number)).start()

def handle_client_connection(client_socket):
    global OSICS_Laser_resourse
    laser_channel_id = 0
    while True:
        # data from PC
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            ticker_start(laser_channel_id)
            break
        request = request.decode('utf-8')
        print(request)
        if(request.startswith('OSICS')):
            command = request.replace('OSICS','')
            with lock_Laser:
                if command.startswith('channel_check:'):
                    laser_channel_id = int(command.split(':')[1])
                    query_response = check_laser_channel(channel_number=laser_channel_id)
                    to_PC_mes = None
                    if query_response == True:
                        to_PC_mes = f'OSICS: CH {laser_channel_id} has locked'
                        laser_channel_id = 1
                    else:
                        available_channels = [channel for channel, status in OSICS_Laser_resourse.items() if status is None]
                        to_PC_mes = "OSICS available_channels: " + ", ".join(available_channels)
                    response_To_PC(client_socket,to_PC_mes)
                elif command.startswith('channel_release'):
                    release_channel_number = int(command.split(':')[1])
                    release_laser_channel(release_channel_number)
                    response_To_PC(client_socket,f'OSICS: CH{release_channel_number} has release')
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