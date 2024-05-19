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

def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            break
        request = request.decode('utf-8')

        if(request.startswith('PM32:')):
            with lock_PM32:
                print("--------------------------")
                print("time",datetime.datetime.now())
                print(request)
                command = request.replace('PM32:','')
                if command.startswith('I?'):
                    channel_number = int(command.split('?')[1])
                    current_data = PM32.i[channel_number]
                    response_To_PC(client_socket,current_data)
                elif command.startswith('Iallvaule?'):
                    channel_string = command.split('?')[1]
                    channel_string = channel_string.strip("[]")
                    channel_list = [int(item) for item in channel_string.split(", ")]
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
    #client_socket.close()



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
