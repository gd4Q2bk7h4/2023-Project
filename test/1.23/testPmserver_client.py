from powermeterlibrary import*
import time
import pyvisa as visa
import numpy as np
import socket

TCP_IP = '192.168.137.212'
TCP_PORT = 5005

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))
 
 
jb_PM = power_meter.PM32(socket=s,channel_list=[0,1,2,3,4,5,6,7])


jb_PM.get_current_value(1)
tmp_channel = [0,1,2,3,4,5,6,7]
jb_PM.get_all_current()