from qontrol import SXInput
import numpy as np


# PM32 = SXInput(serial_port_name='COM9')
# PM32.i[0] = 1*(10**(-6))
# measured_current = PM32.i[0]
# print(type(measured_current))
# print(measured_current)
# print("--")
# channel = [0,1,2,3,4,5,6,7]
# result_array = {}
# while(len(result_array) != len(channel)):
#     for i in channel:
#         data_tmp = PM32.i[i]
#         result_array[i] = data_tmp * (10**6)


# print(result_array)
# print("---")
# print(len(result_array))
# print(result_array[6])

# channel_list=[0,1,2,3,4,5,6,7]
# command = f'PM32:IALL?{channel_list}'
# print(command)
# command_string = command.split('?')[0]
# channel = command.split('?')[1]
# channel = command_string.strip("[]")
# # 分割字符串并转换为整数
# channel= [int(item) for item in command_string.split(", ")]
# print(channel)
# print(type(channel))

channel = [0,1,2,3,4,5]
command = f'nihao{channel}'
print(command)
print(type(command))