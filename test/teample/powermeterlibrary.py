import sys

def send_command(command_string, s):
    # send command
    s.send(command_string.encode())

def recv(s):
    data_size = int(s.recv(8).decode('utf-8'))
    recv_size = 0
    data = b''
    while recv_size < data_size:
        response = s.recv(1024)
        data += response
        recv_size += len(response)
    ack = "ACK".encode()
    s.sendall(ack)
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
            check_laser_avaiable = f'PM32:channel_check?{channel_list}'
            send_command(command_string=check_laser_avaiable,s=self.socket)
            r = recv(s=self.socket)
            if 'valid' in r: #match with record':
                self.channel_List = channel_list
                print(r)
                print('\n')
            else:
                print(r)
                print('\n')
                sys.exit(1)
                
        #get one channel current
        def get_current_value(self,channel_number=0):
            if channel_number in self.channel_List:
                command = f'PM32:I?{channel_number}'
                send_command(command_string=command,s=self.socket)
                current = recv(self.socket)
                print(f'PM32 PD:{channel_number} is {current} mA')
                return current
            else:
                print(f'This channel is not in your selected channel list')
        
        def get_all_current(self):
            command = f'PM32:Iallvaule?{self.channel_List}'
            send_command(command_string=command,s=self.socket)
            current = recv(self.socket)
            print(f'PM32 PD:{self.channel_List} is {current} mA')
            return current