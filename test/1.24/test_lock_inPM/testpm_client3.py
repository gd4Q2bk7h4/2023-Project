from powermeterlibrary import *
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
 
 
jb_PM = power_meter.PM32(socket=s,channel_list=[8,9,10,11])

while True:
    jb_PM.get_current_value(3)
    jb_PM.get_all_current()
    time.sleep(0.9)
    