laser = [
    {"device": "OSICS", "channel": {f"channel_{i}": 'available' for i in range(1, 3)}}  # OSICS has two channels
]

powermemter = [
    {"device": "PM32", "channel": {f"channel_{i}": 'available' for i in range(0, 16)}} #PM32 has 16 channels
]
print(laser['OSICS']['channel']['channel_1'])


# def query_device(device='laser'):
#     result = ""
#     if device == 'laser':
#         for item in laser:
#             device_name = item["device"]
#             device_info = f'{device_name}:\n'
#             for channel, availability in item["channel"].items():
#                 if availability == 'available':
#                     device_info += f'{channel}\n'
#             result += device_info + '\n'
#     elif device == 'powermeter':
#         for item in powermemter:
#             device_name = item["device"]
#             device_info = f'{device_name}:\n'
#             for channel, availability in item["channel"].items():
#                 if availability == 'available':
#                     device_info += f'{channel}\n'
#             result += device_info + '\n'
#     elif device == 'all':
#         print('----')
#         result = query_device('laser')
#         result +=  query_device('powermeter')        
#     return result

# def lock_device_channel(device,laser_name,channel):
#     print(channel)
#     if device == laser:
#         for iteam in laser:
#             if iteam["device"] == laser_name:
#                 for i in channel:
#                   channel_key = f'channel_{i}'
#                   if iteam["channel"][channel_key] == 'available':
#                                     iteam["channel"][channel_key] = 'using'
#                   # iteam["device"][i] = 'using'
#                 break
#             break

# print(query_device('all'))
# lock_device_channel(laser,"OSICS",[1])
# print(query_device('all'))

# laser_record=[]
# laser_record.append('OSCI')
# laser_record.append([1,2,3])
# laser_record=[]
# print(laser_record)
# print(type(laser_record[1]))
# import ast

# # 假设的字符串列表
# string_list = ['[1,2,3]']
# print(string_list)

# # 使用literal_eval转换第一个元素
# actual_list = ast.literal_eval(string_list[0])

# # 输出转换后的列表
# print(actual_list)
