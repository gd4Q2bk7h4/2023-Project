import socket
import serial
import threading
from qontrol import SXInput
import ast
import re

device_timout_time = 20*60 # (mins * secs)

laser = [
    {"device": "OSICS", "CH": {f"CH_{i}": 'available' for i in range(1, 3)}}  # OSICS has two channels
    # {"device": "[LASER NAME]",  "channel": {f"channel_{i}": 'available' for i in range(1, 99)}}   # How to add device
]

powermeter = [
    {"device": "PM32", "PD": {f"PD_{i}": 'available' for i in range(0, 16)}} #PM32 has 16 channels
]

lock_Laser = threading.Lock()
lock_PM32 = threading.Lock()
lock_resource = threading.Lock()

# TCP/IP setting
TCP_IP = '192.168.1.100'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#serial port setting
OSICS_Laser = serial.Serial( # follow by user document of device
    port='/dev/ttyUSB0', #'/dev/ttyUSB0'
    baudrate=9600,         
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    timeout=0.5                
)
PM32 = SXInput(serial_port_name='/dev/ttyUSB1')

def query_device(device='laser'):
    global powermeter
    global laser
    result = ""
    if device == 'laser':
        result += 'Available lasers:\n'
        for item in laser:
            device_name = item["device"]
            device_info = f' {device_name}:\n'
            for channel, availability in item["CH"].items():
                if availability == 'available':
                    device_info += f' {channel}\n'
            result += '- ' + device_info + '\n'
    elif device == 'powermeter':
        result += 'Available powermeters:\n'
        for item in powermeter:
            device_name = item["device"]
            device_info = f' {device_name}:\n'
            for channel, availability in item["PD"].items():
                if availability == 'available':
                    device_info += f' {channel}\n'
            result += '- ' + device_info + '\n'
    elif device == 'all':
        result = query_device('laser')
        result +=  query_device('powermeter')        
    return result

def query_device_channel(device,device_name,query_channel):
    global powermeter
    global laser
    channel_query_result=[]
    if device == 'laser':
        if item["device"] == device_name:
                for i in query_channel:
                    channel_key = f'CH_{i}'
                    if item["CH"][channel_key] == 'available':
                        channel_query_result.append('True')
                else:
                    channel_query_result.append('False') 
    elif device == 'powermeter':
        for item in powermeter:
            for i in query_channel:
                    channel_key = f'PD_{i}'
                    if item["PD"][channel_key] == 'available':
                        channel_query_result.append('True')
                    else:
                        channel_query_result.append('False')
    if False in channel_query_result:
        return False
    else:
        return True

def lock_device_channel(device,device_name,channel,addr):
    if device == 'laser':
        for item in laser:
            print(device_name)
            if item["device"] == device_name:
                for i in channel:
                    channel_key = f'CH_{i}'
                    if item["CH"][channel_key] == 'available':
                        item["CH"][channel_key] = str(addr)
                    else:
                        return False
                return True
    elif device == 'powermeter':
        for item in powermeter:
            if item["device"] == device_name:
                for i in channel:
                    channel_key = f'PD_{i}'
                    if item["PD"][channel_key] == 'available':
                        item["PD"][channel_key] = str(addr)
                    else:
                        return False
                return True

def release_device_channel(device,device_name,channel):
    if device == 'laser':
        for item in laser:
            if item["device"] == device_name:
                for i in channel:
                    channel_key = f'CH_{i}'
                    if not item["CH"][channel_key] == 'available':
                        item["CH"][channel_key] = 'available'
                break
            else:
                break
    elif device == 'powermeter':
        for item in powermeter:
            if item["device"] == device_name:
                for i in channel:
                    channel_key = f'PD_{i}'
                    if not item["PD"][channel_key] == 'available':
                        item["PD"][channel_key] = 'available'
                break
            else:
                break

def OSICS_Laser_transmit(serial,command_string):
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

def response_To_PC(socket,response):
    response = str(response)
    print(response)
    response = response.encode('utf-8')
    data_size = len(response)
    header=bytes(str(data_size),'utf-8').zfill(8)
    try:
        socket.send(header)
        socket.send(response)
    except ConnectionResetError:
        socket.close()
    ack = socket.recv(1024)
    if ack.decode() == "ACK":
        pass
    else:
        print('ERROR: data sending FAIL')

def timeout_operation(laser_name,laser_channel,powermeter_name,powermeter_channel):
    if laser_name != '' and laser_channel != [] and powermeter_name != '' and powermeter_channel != []:
        release_device_channel(device='laser',device_name=laser_name,channel=laser_channel)
        release_device_channel(device='powermeter',device_name=powermeter_name,channel=powermeter_channel)
    print('TIMEOUT: The occupied devices have been released')

def timeout_start(laser_name,laser_channel,powermeter_name,powermeter_channel):
    timer = threading.Timer(device_timout_time, lambda: timeout_operation(laser_name,laser_channel,powermeter_name,powermeter_channel)).start()

def handle_client_connection(client_socket,addr):
    global laser
    global powermeter
    laser_record = ['',[],'']
    powermeter_record = ['',[],'']
    while True:
        # data from PC
        request = client_socket.recv(BUFFER_SIZE)
        # Command timeout
        if not request:
            timeout_start(laser_name=laser_record[0],laser_channel=laser_record[1],powermeter_name=powermeter_record[0],powermeter_channel=powermeter_record[1])
            break
        request = request.decode('utf-8')
        print('-----')
        print(request)

        ### OSICS device control code ------------------
        if(request.startswith('OSICS')):
            with lock_Laser:
                command = request.replace('OSICS','')
                if command.startswith('channel_check:'):
                    laser_channel_id_string = [command.split(':')[1]]
                    laser_channel_id = ast.literal_eval(laser_channel_id_string[0])
                    to_PC_mes = None
                    print(laser_channel_id)
                    if laser_record[0] == 'OSICS' and laser_record[1] == [laser_channel_id] and  laser_record[2] == str(addr):
                        to_PC_mes = f'OSICS: CH [{laser_channel_id}] is a valid device'#match with record'
                    elif laser_record[0] == '' and laser_record[1] == []:
                        to_PC_mes = f'OSICS: please request the resource first'
                    else:
                        to_PC_mes = 'Error: OSICS channel {} is not a valid channel'.format(laser_channel_id_string) #match'
                    response_To_PC(client_socket,to_PC_mes)
                else:
                    to_laser_command = (command + '\r').encode('ascii')
                    laser_result = OSICS_Laser_transmit(serial=OSICS_Laser,command_string=to_laser_command)
                    response_To_PC(client_socket,laser_result)           
        
        ### PM32 device control code ------------------
        elif(request.startswith('PM32:')):
            with lock_PM32:
                command = request.replace('PM32:','')
                if command.startswith('channel_check?'):
                    channel_string = [command.split('?')[1]]
                    to_PC_mes = None
                    PM32_channel_list = ast.literal_eval(channel_string[0])
                    if powermeter_record[0] == 'PM32' and powermeter_record[1] == PM32_channel_list and  powermeter_record[2] == str(addr):
                        to_PC_mes = f'PM32: CH [{PM32_channel_list}] is a valid device'#match with record'
                    else:
                        to_PC_mes = 'Error: PM32 channels {} are not valid channels'.format(channel_string) #match'
                    response_To_PC(client_socket,to_PC_mes)
                elif command.startswith('I?'):
                    channel_number = int(command.split('?')[1])
                    current_data = PM32.i[channel_number]
                    response_To_PC(client_socket,round(current_data,5))
                elif command.startswith('Iallvaule?'):
                    channel_string = [command.split('?')[1]]
                    channel_list = ast.literal_eval(channel_string[0])
                    result_array = []
                    while(len(result_array) != len(channel_list)):
                        for i in channel_list:
                            data_tmp = PM32.i[i]
                            result_array.append(round(data_tmp * (10**6),5))
                    response_To_PC(client_socket,result_array)

        elif(request.startswith('RESOURCE:')):
            with lock_resource:
                command = request.replace('RESOURCE:','')
                if command.startswith('list_available:'):
                    device_check=command.replace('list_available:','')
                    r = str(query_device(device=device_check))
                    response_To_PC(client_socket,r)
                elif command.startswith('access:'):
                    command = command.replace('access:','')
                    mes = ''
                    left_command = command.split(',')
                    lock_device = left_command[0]
                    lock_device_name = left_command[1]
                    lock_channel_string = [re.search(r'\[.*\]', command).group()]
                    lock_channel = ast.literal_eval(lock_channel_string[0])
                    if lock_device == 'laser' and laser_record == ['',[],'']:
                        if lock_device_channel(lock_device,lock_device_name,lock_channel,addr):
                            laser_record[0] = lock_device_name
                            laser_record[1] = lock_channel
                            laser_record[2] = str(addr)
                            mes = f'Access to {lock_device_name}: CH{lock_channel} is GRANTED'
                        else:
                            mes = f'{lock_device_name}: CH{lock_channel} is not avaiable'
                    elif lock_device == 'powermeter' and powermeter_record == ['',[],'']:
                        if lock_device_channel(lock_device,lock_device_name,lock_channel,addr):
                            print('here')
                            powermeter_record[0] = lock_device_name
                            powermeter_record[1] = lock_channel
                            powermeter_record[2] = (str(addr))
                            mes = f'Access to {lock_device_name}: CH{lock_channel} is GRANTED'
                        else:
                            mes = f'{lock_device_name}: CH{lock_channel} is not avaiable'
                    else:
                        mes = 'ERROR: invalid device access command' # You have been locked channel for OSICS'
                    response_To_PC(client_socket,mes)
                elif command.startswith('release:'):
                    command = command.replace('release:','')
                    left_command = command.split(',')
                    release_device = left_command[0]
                    release_device_name = left_command[1]
                    release_channel_string = [re.search(r'\[.*\]', command).group()]
                    release_channel = ast.literal_eval(release_channel_string[0])
                    mes = ''
                    if release_device == 'laser' and laser_record != ['',[],'']:
                        release_device_channel(release_device,release_device_name,release_channel)
                        laser_record = ['',[],'']
                        mes = f'{release_device_name}: CH{release_channel} has been released'
                    elif release_device == 'powermeter' and powermeter_record != ['',[],'']:
                        release_device_channel(release_device,release_device_name,release_channel)
                        powermeter_record = ['',[],'']
                        mes = f'{release_device_name}: CH{release_channel} has been released'
                    else:
                        print(powermeter_record)
                        mes = f'Error: You have released access to the wrong channel for {release_device_name}'
                    response_To_PC(client_socket,f'{mes}')
    print(f'DISCONNECT:{addr}')
    client_socket.close()

def server_main():
    # create socket 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(2)     # Number of PCs to listen to

    print("Please wait, connecting to PC...")

    # 
    while True:
        conn, addr = s.accept()
        print('CONNECTED to IP address：', addr)
        client_thread = threading.Thread(target=handle_client_connection, args=(conn,addr))
        client_thread.start()

if __name__ == '__main__':
    server_main()