import socket
import serial
import threading
import vxi11
from qontrol import SXInput
from serverlibrary import*

laser = [
    {"device": "OSICS", "CH": {f"CH_{i}": 'available' for i in range(1, 3)}},  # OSICS has two channels
    {"device": "QUANTIFI",  "CH": {f"CH_{i}": 'available' for i in range(1, 2)}}   # How to add device
]

powermeter = [
    {"device": "PM32", "PD": {f"PD_{i}": 'available' for i in range(0, 16)}} #PM32 has 16 channels
]

lock_Laser_OSICS = threading.Lock()
lock_PM32 = threading.Lock()
lock_resource = threading.Lock()
lock_Laser_Quantifi = threading.Lock()

# TCP/IP setting
TCP_IP = '192.168.1.100'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#serial port setting
#laser
OSICS_Laser = serial.Serial( # follow by user document of device
    port='/dev/ttyUSB0', #'/dev/ttyUSB0'
    baudrate=9600,         
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    timeout=0.5                
)
Quantifi_laser = vxi11.Instrument("192.168.101.201")
#photodiode array
PM32 = SXInput(serial_port_name='/dev/ttyUSB1')

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
            with lock_Laser_OSICS:
                control_OSICS(request=request,addr=addr,client_socket=client_socket,OSICS_Laser=OSICS_Laser,laser_record=laser_record,laser_dictionary=laser,powermeter_dictionary=powermeter)
        elif(request.startswith('QUANTIFI')):
            with lock_Laser_Quantifi:
                control_Quantifi(request=request,addr=addr,client_socket=client_socket,laser_record=laser_record,laser_dictionary=laser,powermeter_dictionary=powermeter,Quantifi_laser=Quantifi_laser)
        ### PM32 device control code ------------------
        elif(request.startswith('PM32:')):
            with lock_PM32:
                control_PM32(request=request,addr=addr,client_socket=client_socket,PM32=PM32,powermeter_record=powermeter_record,laser_dictionary=laser,powermeter_dictionary=powermeter)
        elif(request.startswith('RESOURCE:')):
            with lock_resource:
                control_Rescource_manager(request=request,client_socket=client_socket,addr=addr,laser_record=laser_record,powermeter_record=powermeter_record,laser_dictionary=laser,powermeter_dictionary=powermeter)
    print(f'DISCONNECT:{addr}')
    client_socket.close()

def server_main():
    # create socket 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)     # Number of PCs to listen to

    print("Please wait, connecting to PC...")

    # 
    while True:
        conn, addr = s.accept()
        print('CONNECTED to IP address：', addr)
        client_thread = threading.Thread(target=handle_client_connection, args=(conn,addr))
        client_thread.start()

if __name__ == '__main__':
    server_main()