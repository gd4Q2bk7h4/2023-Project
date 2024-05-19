import threading
import ast
import re

device_timout_time = 20*60 # (mins * secs)

def query_device(device,laser_dictionary,powermeter_dictionary):
    result = ""
    if device == 'laser':
        result += 'Available lasers:\n'
        for item in laser_dictionary:
            device_name = item["device"]
            device_info = f' {device_name}:\n'
            for channel, availability in item["CH"].items():
                if availability == 'available':
                    device_info += f' {channel}\n'
            result += '- ' + device_info + '\n'
    elif device == 'powermeter':
        result += 'Available powermeters:\n'
        for item in powermeter_dictionary:
            device_name = item["device"]
            device_info = f' {device_name}:\n'
            for channel, availability in item["PD"].items():
                if availability == 'available':
                    device_info += f' {channel}\n'
            result += '- ' + device_info + '\n'
    elif device == 'all':
        result = query_device('laser',laser_dictionary,powermeter_dictionary)
        result +=  query_device('powermeter',laser_dictionary,powermeter_dictionary)        
    return result

def query_device_IP(device,device_name,query_channel,addr,laser_dictionary,powermeter_dictionary):
    channel_query_result=[]
    if device == 'laser':
        for item in laser_dictionary:
            if item["device"] == device_name:
                    for i in query_channel:
                        channel_key = f'CH_{i}'
                        if item["CH"][channel_key] == str(addr[0]):
                            channel_query_result.append('True')
                    else:
                        channel_query_result.append('False') 
    elif device == 'powermeter':
        for item in powermeter_dictionary:
            for i in query_channel:
                    channel_key = f'PD_{i}'
                    if item["PD"][channel_key] == str(addr[0]):
                        channel_query_result.append('True')
                    else:
                        channel_query_result.append('False')
    if False in channel_query_result:
        return False
    else:
        return True

def lock_device_channel(device,device_name,channel,addr,laser_dictionary,powermeter_dictionary):
    if device == 'laser':
        for item in laser_dictionary:
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
        for item in powermeter_dictionary:
            if item["device"] == device_name:
                for i in channel:
                    channel_key = f'PD_{i}'
                    if item["PD"][channel_key] == 'available':
                        item["PD"][channel_key] = str(addr)
                    else:
                        return False
                return True

def release_device_channel(device,device_name,channel,laser_dictionary,powermeter_dictionary):
    if device == 'laser':
        for item in laser_dictionary:
            if item["device"] == device_name:
                for i in channel:
                    channel_key = f'CH_{i}'
                    if not item["CH"][channel_key] == 'available':
                        item["CH"][channel_key] = 'available'
                break
            else:
                break
    elif device == 'powermeter':
        for item in powermeter_dictionary:
            if item["device"] == device_name:
                for i in channel:
                    channel_key = f'PD_{i}'
                    if not item["PD"][channel_key] == 'available':
                        item["PD"][channel_key] = 'available'
                break
            else:
                break

def OSICS_Laser_transmit(ser,command_string):
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
    ser.close()
    return outputData
    # if not serial.is_open:
    #     serial.open()
    # serial.write(command_string)
    # try :
    #     while True:
    #         outputData = serial.readline()
    #         if outputData:
    #             outputData  = outputData.decode('utf-8').strip()
    #             outputData = outputData.replace('\r>', '')
    #             break
    # except KeyboardInterrupt:
    #     print("program end")
    # serial.close()
    # return outputData

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

def timeout_operation(laser_name,laser_channel,powermeter_name,powermeter_channel,laser_dictionary,powermeter_dictionary):
    if laser_name != '' and laser_channel != [] and powermeter_name != '' and powermeter_channel != []:
        release_device_channel(device='laser',device_name=laser_name,channel=laser_channel,laser_dictionary=laser_dictionary,powermeter_dictionary=powermeter_dictionary)
        release_device_channel(device='powermeter',device_name=powermeter_name,channel=powermeter_channel,laser_dictionary=laser_dictionary,powermeter_dictionary=powermeter_dictionary)
    print('TIMEOUT: The occupied devices have been released')

def timeout_start(laser_name,laser_channel,powermeter_name,powermeter_channel):
    timer = threading.Timer(device_timout_time, lambda: timeout_operation(laser_name,laser_channel,powermeter_name,powermeter_channel)).start()

def control_OSICS(request,addr,client_socket,OSICS_Laser,laser_record,laser_dictionary,powermeter_dictionary):
    command = request.replace('OSICS','')
    if command.startswith('channel_check:'):
        laser_channel_id_string = [command.split(':')[1]]
        laser_channel_id = [ast.literal_eval(laser_channel_id_string[0])]
        print(laser_channel_id)
        print(type(laser_channel_id))
        to_PC_mes = None
        if query_device_IP('laser','OSICS',laser_channel_id,addr,laser_dictionary,powermeter_dictionary):
            to_PC_mes = f'OSICS: CH {laser_channel_id} is a valid device'#match with record'
        elif laser_record[0] == '' and laser_record[1] == []:
            to_PC_mes = f'OSICS: please request the resource first'
        else:
            to_PC_mes = 'Error: OSICS channel {} is not a valid channel'.format(laser_channel_id_string) #match'
        response_To_PC(client_socket,to_PC_mes)
    else:
        to_laser_command = (command + '\r').encode('ascii')
        laser_result = OSICS_Laser_transmit(serial=OSICS_Laser,command_string=to_laser_command)
        response_To_PC(client_socket,laser_result)

def control_PM32(request,addr,client_socket,PM32,powermeter_record,laser_dictionary,powermeter_dictionary):
    command = request.replace('PM32:','')
    if command.startswith('channel_check?'):
        channel_string = [command.split('?')[1]]
        to_PC_mes = None
        PM32_channel_list = ast.literal_eval(channel_string[0])
        if query_device_IP('powermeter','PM32',PM32_channel_list,addr,laser_dictionary,powermeter_dictionary):
            to_PC_mes = f'PM32: CH [{PM32_channel_list}] is a valid device'#match with record'
        elif powermeter_record[0] == '' and powermeter_record[1] == []:
            to_PC_mes = f'PM32: please request the resource first'
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
                result_array.append(round(PM32.i[i]* (10**6),5))
        response_To_PC(client_socket,result_array)

def control_Rescource_manager(request,client_socket,addr,laser_record,powermeter_record,laser_dictionary,powermeter_dictionary):
    command = request.replace('RESOURCE:','')
    if command.startswith('list_available:'):
        device_check=command.replace('list_available:','')
        r = str(query_device(device_check,laser_dictionary,powermeter_dictionary))
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
            if lock_device_channel(lock_device,lock_device_name,lock_channel,addr,laser_dictionary,powermeter_dictionary):
                laser_record[0] = lock_device_name
                laser_record[1] = lock_channel
                laser_record[2] = str(addr[0])
                mes = f'Access to {lock_device_name}: CH{lock_channel} is GRANTED'
            else:
                mes = f'{lock_device_name}: CH{lock_channel} is not avaiable'
        elif lock_device == 'powermeter' and powermeter_record == ['',[],'']:
            if lock_device_channel(lock_device,lock_device_name,lock_channel,addr,laser_dictionary,powermeter_dictionary):
                print('here')
                powermeter_record[0] = lock_device_name
                powermeter_record[1] = lock_channel
                powermeter_record[2] = (str(addr[0]))
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
        if release_device == 'laser':
            release_device_channel(release_device,release_device_name,release_channel,laser_dictionary,powermeter_dictionary)
            laser_record = ['',[],'']
            mes = f'{release_device_name}: CH{release_channel} has been released'
        elif release_device == 'powermeter':
            release_device_channel(release_device,release_device_name,release_channel,laser_dictionary,powermeter_dictionary)
            powermeter_record = ['',[],'']
            mes = f'{release_device_name}: CH{release_channel} has been released'
        else:
            mes = f'Error: You have released access to the wrong channel for {release_device_name}'
        response_To_PC(client_socket,f'{mes}')