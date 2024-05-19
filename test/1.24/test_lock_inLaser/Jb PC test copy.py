
from laserlibrary import *
import time
import pyvisa as visa
import numpy as np
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))
 
 
jb_laser = laser.OSICSLaser(socket=s)
 
start_wavelength = 1500
stop_wavelength = 1550
num_steps = 5
 
wavelengths = np.linspace(start=start_wavelength, stop=stop_wavelength, num=num_steps)
 
 
if __name__ == '__main__':
    time.sleep(3)
    jb_laser.set_wavelength(channel_number=1, value=start_wavelength)
    jb_laser.set_power_unit_dBm(channel_number=1)
    jb_laser.set_output_power(channel_number=1, value=4)
    time.sleep(5)
    jb_laser.enable_channel(1)
    time.sleep(2)
 
    for i, wavelength in enumerate(wavelengths):
        jb_laser.set_wavelength(channel_number=1, value=wavelength)
        time.sleep(2)
        ### read photodiodes/powermeter
        print(f"Laser set to {wavelength} nm at {1}")
 
    jb_laser.disable_channel(channel_number=1)