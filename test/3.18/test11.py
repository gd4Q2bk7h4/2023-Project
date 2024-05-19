

laser = [
    {"device": "OSICS", "CH": {f"CH_{i}": 'available' for i in range(1, 3)}},  # OSICS has two channels
    {"device": "QUANTIFI",  "CH": {f"CH_{i}": 'available' for i in range(1, 2)}}   # How to add device
]
for item in laser:
                  print(item["device"])
                  if item["device"] == "QUANTIFI":
                     print('test')
                     for i in [1]:
                                    channel_key = f'CH_{i}'
                                    if item["CH"][channel_key] == 'available':
                                                      item["CH"][channel_key] = 'available'
                                                      print(laser)
                                                      break
                                                      
                                    else:
                                                      break