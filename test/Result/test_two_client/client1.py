from laserlibrary import *
import time
import pyvisa as visa
import numpy as np
import socket
from resourcelibrary import*
from powermeterlibrary import*
import time

#TCP/IP setting
TCP_IP = '192.168.1.100'
TCP_PORT = 5005
# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))


#create the laser and powermeter
used_laser = laser.OSICSLaser(socket=s,channel_number=1)
PM = power_meter.PM32(socket=s,channel_list=[0,1,2,3,4,5,6,7])

start_wavelength = 1500
stop_wavelength = 1550
num_steps = 5
 
wavelengths = np.linspace(start=start_wavelength, stop=stop_wavelength, num=num_steps)
 
 
if __name__ == '__main__':
    start_time = time.time()
    used_laser.set_wavelength(value=start_wavelength)
    used_laser.set_power_unit_mW()
    used_laser.set_power_unit_dBm()
    used_laser.set_output_power(value=-3)
    time.sleep(5)
    used_laser.query_wavelength()
    used_laser.enable_channel()
    for i, wavelength in enumerate(wavelengths):
        used_laser.set_wavelength(value=wavelength)
        time.sleep(2)
        current = PM.get_all_current()
        ### read photodiodes/powermeter
        print(f"Laser set to {wavelength} nm at {1}")
        print(f'current is {current} mA')
 
    used_laser.disable_channel()
