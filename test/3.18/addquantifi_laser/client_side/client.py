from laserlibrary import *
import time
import pyvisa as visa
import numpy as np
import socket
from resourcelibrary import*
from powermeterlibrary import*
def run_all_methods(obj):
    methods = [method for method in dir(obj) if callable(getattr(obj, method)) and method.startswith('__') is False]
    for method in methods:
        getattr(obj, method)()
#TCP/IP setting
TCP_IP = '192.168.1.100'
TCP_PORT = 5005
# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))

manager = resource_manager(socket=s)
manager.list_available_resource('all')
manager.request_access('laser','QUANTIFI',[1])
manager.request_access('powermeter','PM32',[4,5,6,7])
PM = power_meter.PM32(socket=s,channel_list=[4,5,6,7])
quantifi_laser= laser.Quantifi(socket=s,channel_number=1)

start_wavelength = 1500
stop_wavelength = 1550
num_steps = 5
 
wavelengths = np.linspace(start=start_wavelength, stop=stop_wavelength, num=num_steps)
if __name__ == '__main__':
                  quantifi_laser.switch_on()
                  quantifi_laser.set_laser_power(10)
                  for i, wavelength in enumerate(wavelengths):
                                    quantifi_laser.set_laser_wavelength(wavelength)
                                    time.sleep(1)
                                    current = PM.get_all_current()
                                    ### read photodiodes/powermeter
                                    print(f"Laser set to {wavelength} nm at {1}")
                                    print(f'current is {current} mA')
                  quantifi_laser.switch_off()
                  manager.release_resource('laser','QUANTIFI',[1])
                  manager.release_resource('powermeter','PM32',[4,5,6,7])
                  manager.list_available_resource('all')
