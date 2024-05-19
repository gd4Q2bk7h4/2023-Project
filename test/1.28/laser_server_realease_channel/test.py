# 创建包含两个channel的字典
channels_status = {f'channel_{i}': None for i in range(1, 3)}

def occupy_channel(channel_number):
    """占用指定的channel"""
    global channels_status
    channel_key = f'channel_{channel_number}'
    if channel_key in channels_status:
        if channels_status[channel_key] is None:
            channels_status[channel_key] = 'occupied'
            print(f"{channel_key} 已被占用.")
        else:
            print(f"{channel_key} 已经被占用，无法再次占用.")
    else:
        print(f"{channel_key} 不存在.")

def check_available_channels():
    """检查并打印所有可用的channels"""
    available_channels = [channel for channel, status in channels_status.items() if status is None]
    print("可用的channels: " + ", ".join(available_channels))

# 示例：尝试占用channel_1
occupy_channel(1)

# 检查并打印可用的channels
check_available_channels()

# 再次尝试占用channel_1
occupy_channel(1)
