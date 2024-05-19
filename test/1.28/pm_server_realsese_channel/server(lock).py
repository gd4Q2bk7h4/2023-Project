import socket
import serial
import threading
import qontrol
import datetime

# TCP/IP settting
#TCP_IP = '192.168.137.212'
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

lock_PM32 = threading.Lock()
PM32_resourse = {f'CH{i}': None for i in range(0, 16)}

PM32 = qontrol.SXInput(serial_port_name='COM9')

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

def check_PM32_channel(channel_list):
    global PM32_resourse
    status_channels = []
    for i in channel_list:
        channel_key = f'CH{i}'
        if PM32_resourse[channel_key] is None:
            status_channels.append(0)
            PM32_resourse[channel_key] = 'using'
        else:
            status_channels.append(1)
    if 1 in status_channels:
        return False
    else:
        return True

def release_PM32_channel(channel_number):
    global PM32_resourse
    for i in channel_number:
        if not PM32_resourse[i] is None:
            PM32_resourse[i] = None

def ticker_opreation(channel_number):
    print('time out')
    release_PM32_channel(channel_number)
    print('The device resources has release')

def ticker_start(channel_number):
    timer = threading.Timer(20,lambda: ticker_opreation(channel_number)).start()

def handle_client_connection(client_socket):
    PM32_channel_list=[]
    while True:
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            ticker_start(PM32_channel_list)
            break
        request = request.decode('utf-8')

        if(request.startswith('PM32:')):
            with lock_PM32:
                command = request.replace('PM32:','')
                if command.startswith('channel_check?'):
                    channel_string = command.split('?')[1]
                    channel_string = channel_string.strip("[]")
                    PM32_channel_list = [int(item) for item in channel_string.split(",")]
                    query_response = check_PM32_channel(channel_list=PM32_channel_list)
                    to_PC_mes = None
                    if query_response == True:
                        to_PC_mes = f'PM32: CH {PM32_channel_list} has locked'
                    else:
                        available_channels = [channel for channel, status in PM32_resourse.items() if status is None]
                        to_PC_mes = "PM32 available_channels: " + ", ".join(available_channels)
                    response_To_PC(client_socket,to_PC_mes)
                elif command.startswith('channel_list_release'):
                    release_channel_list = int(command.split(':')[1])
                    release_PM32_channel(release_channel_list)
                    response_To_PC(client_socket,f'PM32: CH{release_channel_list} has release')
                elif command.startswith('I?'):
                    channel_number = int(command.split('?')[1])
                    current_data = PM32.i[channel_number]
                    response_To_PC(client_socket,current_data)
                elif command.startswith('Iallvaule?'):
                    channel_string = command.split('?')[1]
                    channel_string = channel_string.strip("[]")
                    channel_list = [int(item) for item in channel_string.split(",")]
                    result_array = []
                    while(len(result_array) != len(channel_list)):
                        for i in channel_list:
                            data_tmp = PM32.i[i]
                            result_array.append(data_tmp * (10**6))
                    response_To_PC(client_socket,result_array)
                elif command.startswith('Iallvauleset?'):
                    channel_list_and_value = request.replace('PM32:Iallvauleset?','')
                    channel_list_string = channel_list_and_value.split(']')[0]
                    channel_list = [int(item) for item in channel_list_string .split(", ")]
                    current_value = int(channel_list_and_value.split(']')[1])
                    for i in channel_list:
                        PM32.i[i] = current_value
                    response_To_PC("OK")
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
