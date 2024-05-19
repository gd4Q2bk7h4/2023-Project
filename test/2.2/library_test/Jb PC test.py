from laserlibrary import *
import time
import pyvisa as visa
import numpy as np
import socket
from resourcelibrary import*
from powermeterlibrary import*

#TCP/IP setting
TCP_IP = '192.168.1.100'
TCP_PORT = 5005
# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))

jb_resource_manager = resource_manager(socket=s)
# jb_resource_manager.release_resource('laser','OSICS',[1])
# jb_resource_manager.release_resource('powermeter','PM32',[4,5,6,7])

jb_resource_manager.list_available_resource('all')

jb_resource_manager.request_access('laser','OSICS',[1])
jb_resource_manager.request_access('powermeter','PM32',[4,5,6,7])

jb_laser = laser.OSICSLaser(socket=s,channel_number=1)
jb_PM = power_meter.PM32(socket=s,channel_list=[4,5,6,7])

jb_resource_manager.list_available_resource('all')

# jb_resource_manager.release_resource('laser','OSICS',[1])
# jb_resource_manager.list_available_resource('laser')
 
start_wavelength = 1500
stop_wavelength = 1550
num_steps = 5
 
wavelengths = np.linspace(start=start_wavelength, stop=stop_wavelength, num=num_steps)
 
 
if __name__ == '__main__':
    
    jb_laser.set_wavelength(value=start_wavelength)
    jb_laser.set_power_unit_mW()
    jb_laser.set_power_unit_dBm()
    jb_laser.set_output_power(value=-3)
    time.sleep(5)
    jb_laser.query_wavelength()
    jb_laser.enable_channel()
    for i, wavelength in enumerate(wavelengths):
        jb_laser.set_wavelength(value=wavelength)
        time.sleep(2)
        current = jb_PM.get_all_current()
        ### read photodiodes/powermeter
        # print(f"Laser set to {wavelength} nm at {1}")
        # print(f'current is {current} mA')
 
    jb_laser.disable_channel()
    jb_resource_manager.list_available_resource('all')
    jb_resource_manager.release_resource('laser','OSICS',[1])
    jb_resource_manager.release_resource('powermeter','PM32',[4,5,6,7])
    jb_resource_manager.list_available_resource('all')