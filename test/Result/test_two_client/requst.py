from resourcelibrary import*
import socket
#TCP/IP setting
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