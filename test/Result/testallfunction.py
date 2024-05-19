from laserlibrary import *
import time
import socket
from resourcelibrary import*
from powermeterlibrary import*


def run_all_methods(obj):
    methods = [method for method in dir(obj) if callable(getattr(obj, method)) and method.startswith('__') is False]
    for method in methods:
        getattr(obj, method)()

TCP_IP = '192.168.1.100'
TCP_PORT = 5005
# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))

manager = resource_manager(socket=s)
manager.list_available_resource('all')

#requset the device resources
manager.request_access('laser','OSICS',[1])
manager.request_access('powermeter','PM32',[0,1,2,3,4,5,6,7])
#create the laser and powermeter
used_laser = laser.OSICSLaser(socket=s,channel_number=1)
PM = power_meter.PM32(socket=s,channel_list=[0,1,2,3,4,5,6,7])

record_time_list = []
Total_time = 0
for i in range(10):
    start_time = time.time()
    run_all_methods(used_laser)
    run_all_methods(PM)
    end_time = time.time()
    record_time_list.append(f'The test all function NO.{i+1} tme cost:{end_time - start_time} seconds')
    Total_time += end_time - start_time

for i in record_time_list:
    print(i)

print(f'The total time of ten tests is {Total_time}')
print(f'The average time of one test is {Total_time/10}')