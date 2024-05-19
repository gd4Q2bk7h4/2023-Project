import socket
from laserlibrary import laser

TCP_IP = '192.168.137.48'
TCP_PORT = 5005

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect
s.connect((TCP_IP, TCP_PORT))

OSICS_Laser = laser.OSICSLaser(socket=s)

# OSICS_Laser.enable_channel(1)
# OSICS_Laser.query_channel_state(1)
# OSICS_Laser.set_spectral_unit_GHZ(1)
# OSICS_Laser.query_channel_spectral_unit(1)
# OSICS_Laser.set_spectral_unit_nm(1)
# OSICS_Laser.query_channel_spectral_unit(1)
# OSICS_Laser.set_power_unit_dBm(1)
# OSICS_Laser.query_channel_power_unit(1)
# OSICS_Laser.set_power_unit_mW(1)
# OSICS_Laser.query_channel_power_unit(1)
# OSICS_Laser.set_power_unit_dBm(1)
# OSICS_Laser.set_output_power(1,1550)
# OSICS_Laser.query_output_power(1)
# OSICS_Laser.query_output_power(1)
# OSICS_Laser.query_channel_state(1)
# OSICS_Laser.query_current(1)
# OSICS_Laser.query_current_max(1)
# OSICS_Laser.disable_channel(1)

OSICS_Laser.enable_channel(1)
OSICS_Laser.query_channel_power_unit(1)
OSICS_Laser.set_output_power(1,11.6)
OSICS_Laser.disable_channel(1)