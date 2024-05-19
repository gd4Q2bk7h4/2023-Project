def send_command(command_string, s):
    # send command
    s.send(command_string.encode())
    print(command_string.encode())

def recv(s):
    data_size = int(s.recv(8).decode('utf-8'))
    recv_size = 0
    data = b''
    while recv_size < data_size:
        response = s.recv(1024)
        data += response
        recv_size += len(response)
    return data.decode('utf-8')

class power_meter(object):
    """
    can extend your power meter class in here
    don't forget import the package
    """
    def __init__(self,socket):
            # Defaults
            self.socket = socket #IP address

    class PM32(object):
        def __init__(self,socket,channel_list=[0,1,2,3,4,5,6,7]):
            # Defaults
            self.socket = socket #IP address
            self.channel_List = str(channel_list)
        
        #locj the array channel
        def lock_set_of_array_channel(self):
            command = f'PM32:channelslock,{self.channel_List}'
            send_command(command_string=command)
            res = recv(self.socket)
            print(res)
        
        #release the array channel
        def release_set_of_array_channel(self):
            command = f'PM32:channelrelease,{self.channel_List}'
            send_command(command_string=command)
            res = recv(self.socket)
            print(res)
        
        #get one channel current
        def get_current_value(self,channel_number=0):
            command = f'PM32:I?{channel_number}，0'
            send_command(command_string=command,s=self.socket)
            current = recv(self.socket)
            print(f'The current of channel {channel_number} is {current}')
            return current
        
        def get_all_current(self):
            command = f'PM32:Iallvaule?{self.channel_List},0'
            send_command(command_string=command,s=self.socket)
            current = recv(self.socket)
            print(f'The current of channel {self.channel_List} is {current}')
            return current
        
        def set_all_current(self,value):
            command = f'PM32:Iallvauleset?{self.channel_List},{value}'
            send_command(command_string=command,s=self.socket)
            current = recv(self.socket)
            print(f'The current of channel {self.channel_List} has set to {current}')