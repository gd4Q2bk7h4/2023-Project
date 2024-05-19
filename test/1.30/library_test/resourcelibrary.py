import sys
device_list = ['laser','powermeter']
device_name_list = {'OSICS':[1,2],'PM32':[i for i in range(16)]}

def send_command(command_string, socket):
    # send command
    socket.send(command_string.encode())

def recv(socket):
    data_size = int(socket.recv(8).decode('utf-8'))
    recv_size = 0
    data = b''
    while recv_size < data_size:
        response = socket.recv(1024)
        data += response
        recv_size += len(response)
    ack = "ACK".encode()
    socket.sendall(ack)
    return data.decode('utf-8')
class resource_manager(object):

    def __init__(self,socket):
        self.socket = socket

    def list_available_resource(self,device):
        command = None
        if device =='laser':
            command = f'RESOURCE:list_available:laser'
        elif device == 'powermeter':
            command = f'RESOURCE:list_available:powermeter'
        elif device == 'all':
            command = f'RESOURCE:list_available:all'
        else:
            print('invalid opreation')
            sys.exit(1)
        send_command(command_string=command,socket=self.socket)
        r=recv(socket=self.socket)
        print(r)

    def request_access(self,device='laser',device_name='OSICS',channel_or_channelList=[1]):
        if device in device_list and device_name in device_name_list:
            if set(channel_or_channelList).issubset(set(device_name_list[device_name])):
                commnad = f'RESOURCE:access:{device},{device_name},{channel_or_channelList}'
                send_command(command_string=commnad,socket=self.socket)
                r=recv(socket=self.socket)
                print(r)
                if r == f'{device_name}: CH{channel_or_channelList} is not avaiable':
                    sys.exit(1)
            else:
                print(f'invaild channel, pick in {device_name} {device_name_list[device_name]}')
                sys.exit(1)
        else:
            if device not in device_list and device_name not in device_name_list:
                print(f'invaild device, pick in {device_list}')
                print(f'invaild device name, pick in {device_name_list}')
            elif device not in device_list:
                print(f'invaild device, pick in {device_list}')
            elif device_name not in device_name_list:
                print(f'invaild device name, pick in {device_name_list}')
            sys.exit(1)

    def release_resource(self,device,device_name,channel_or_channelList):
        if device in device_list and device_name in device_name_list:
            if set(channel_or_channelList).issubset(set(device_name_list[device_name])) :
                commnad = f'RESOURCE:release:{device},{device_name},{channel_or_channelList}'
                send_command(command_string=commnad,socket=self.socket)
                r=recv(socket=self.socket)
                print(r)
            else:
                print(f'invaild channel, pick in {device_name} {device_name_list[device_name]}')
                sys.exit(1)
        else:
            if device not in device_list and device_name not in device_name_list:
                print(f'invaild device, pick in {device_list}')
                print(f'invaild device name, pick in {device_name_list}')
            elif device not in device_list:
                print(f'invaild device, pick in {device_list}')
            elif device_name not in device_name_list:
                print(f'invaild device name, pick in {device_name_list}')
            sys.exit(1)