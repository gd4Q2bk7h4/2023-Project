import socket
import serial
import threading
from qontrol import SXInput
import ast

record_OSICS = 0
record_PM32_start = 0
OSICS_Laser_resourse = [True,True]
PM32_resource = [True]*16
lock = threading.Lock()

# TCP/IP settting
TCP_IP = '192.168.137.212'
TCP_PORT = 5005
BUFFER_SIZE = 1024

OSICS_Laser = serial.Serial( # follow by user document of device
    port='/dev/ttyUSB0', #'/dev/ttyUSB0'
    baudrate=9600,         
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    timeout=0.5                
)

PM32 = SXInput(serial_port_name='/dev/ttyUSB1')

def OSCII_Laser_transimit(serial,command_string):
    if not serial.is_open:
        serial.open
    serial.write(command_string)
    print(command_string)
    outputData = serial.readline()
    outputData  = outputData.decode('utf-8').strip()
    outputData = outputData.replace('\r>', '')
    serial.close()
    return outputData

def PM32_transimit(command_string, channel,value=0):
    data_send = 0
    if command_string.upper() == 'I?':
        data_send = PM32.get_value(channel,para='I')
    elif command_string.upper() == 'IALL?':
        for i in channel:
            data_tmp = PM32.get_value(i,para='I')
            data_send += f'{data_tmp},'
    elif command_string.upper() == 'IALLVALUESET':
        PM32.set_all_values(para='I',values=value)
        data_send = f'The current has been set to {value}'
    
    return data_send

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

def handle_client_connection(client_socket,lock):
    while True:
        # data from PC
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            break
        request = request.decode('utf-8')
        print(request)
        with lock:
            if(request.startswith('OSICS')):
                command = request.replace('OSICS','')
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
                    laser_reuslt = OSCII_Laser_transimit(to_laser_command,OSICS_Laser)
                    response_To_PC(laser_reuslt)
            elif(request.startswith('PM32:')):
                command = request.replace('PM32:','')
                if command.startswith('channellock:'):
                    lock_channel = command.split(',')[1]
                    lock_channel = ast.literal_eval(lock_channel)
                    lock_state = check_value_in_list(lock_channel,PM32_resource)
                    if lock_state == True:
                        for index in lock_channel:
                            PM32_resource[index] = False
                        response_To_PC(client_socket,'The channel of PM32 has been lock')
                    else:
                        available_PM32 = [str(index) for index, value in enumerate(PM32_resource) if not value]
                        response = f'Error,The avaiable laser channel is {available_PM32}'
                        response_To_PC(socket,response)
                elif command.startswith('channellock:'):
                    release_channel_PM32 = command.split(',')[1]
                    release_channel_PM32 = ast.literal_eval(lock_channel)
                    for index in release_channel_PM32:
                        PM32_resource[index] == True
                    response_To_PC(client_socket,'The channel of PM32 has been release')
                else:
                    command_string = command.split('?')[0]
                    if command_string.startswith('Iallvaule'):
                        start = command_string.find('[')
                        end = command_string.find(']', start)
                        last_comma_index = command_string.rfind(',')
                        if start != -1 and end != -1:
                            channel_list = command_string[start:end+1]
                        else:
                            channel_list = ''
                        channel_number_to_PM32 = channel_list
                        if last_comma_index != -1:
                            tmp_value = command_string[last_comma_index + 1:]
                        else:
                            tmp_value = ''
                        value_to_PM32 = tmp_value
                    recv=PM32_transimit(command_string=command_string,channel=channel_number_to_PM32,value=value_to_PM32)
                    response_To_PC(client_socket,recv)
            else:
                response_To_PC(client_socket,'Error Command')

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