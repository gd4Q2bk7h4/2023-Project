import socket
import serial
import threading
import qontrol

# TCP/IP settting
TCP_IP = '172.21.91.181'
TCP_PORT = 5005
BUFFER_SIZE = 1024

laserSerial = serial.Serial( # follow by user document of device
    port='COM6', #'/dev/ttyUSB0'
    baudrate=9600,         
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    timeout=1                
)
PM32 = qontrol.SXInput(serial_port_name='COM5')
PM32.get_value(0, 'I')

laserHelpInformation = {
    'CH#:DISABLE' : 'Disables the laser output of the T100 module',
    'CH#:ENABLE' : 'Enable the laser output of the T100 module',
    'CH#:ENABLE?' : 'Returns the state of the laser-output control on the T100 module',
    'CH#:GHZ' : 'Sets GHZ as the spectral unit of module',
    'CH#:NM'  : 'Sets nm as the spectral unit of module',
    'CH#:NM?' : 'Return the actual spectral unit',
    'CH#:DBM' : 'Sets dBm as the power unit of the module',
    'CH#:MW' : 'Sets mW as the power unit of the module',
    'CH#:MW?' : 'Returns the actual power unit',
    'CH#:P=' : 'Sets the optical output-power of the module depending on the selected power unit',
    'CH#:LIMIT?' : 'Returns the state of the output power.',
    'CH#:I?' : 'Returns the present current level in mA.',
    'CH#:IMAX?' : 'Returns the diode maximum current in mA.',
    'CH#:L=' : 'syntax:CH#:L=xxxx.xxx (#: slot number of the module, in the range 1 to 8. xxxx.xxx: the emission wavelength value in nm.)',
    'CH#:L?' : 'Returns the emission wavelength of the module in nm.',
    'CH#:F=' : 'Sets the emission frequency of the module in GHz.',
    'CH#:F?' : 'Returns the emission frequency of the module in GHz.',
    'CH#:CTRL' : 'Enables/disables the Auto-peak Find function.',
    'CH#:APF?' : 'Returns the state of the Auto-peak Find function.',
    'CH#:MOD_CTRL' : '	Description	Sets the digital (TTL) modulation of the T100 module optical signal. If you apply analog modulation directly via the SMB subclic connector at the module BKR faceplate, you must set this function to disable all pending digital modulation.',
    'CH#:MOD_CTRL?' : 'Returns the selected modulation activation state.',
    'CH#:MOD_SRC'   : 'Sets the modulation source of the T100 module.',
    'CH#:MOD_F=' :'Sets the frequency of the T100 module INTERNAL digital (TTL) modulation source.',
    'CH#:MOD_F?' : 'Returns the frequency selected for the internal modulation generator in Hz.',
    'CH#:MOD_SRC?' : 'Returns the selected modulation source.',
    'CH#:WAVEREF' : 'Runs the internal wavelength referencing procedure.',
    'CH#:LCAL1=' : 'Sets the first wavelength value of the two-point wavelength calibration method.',
    'CH#:LCAL2=' : 'Sets the second wavelength value of the two-point wavelength calibration method. LCAL2 is the second factory calibration wavelength (in nm only).',
    'CH#:LCAL1?' : 'Returns the first calibration wavelength of the two-point wavelength calibration method.',
    'CH#:LCAL2?' : 'Returns the second calibration wavelength of the two-point wavelength calibration method',
    'CH#:PCAL1=' : 'Sets the first power value of the two-point power calibration method. This value corresponds to the lower limit of the T100 module wavelength-range.',
    'CH#:PCAL2=' : 'Sets the second power-value of the two-point power calibration method.',
    'CH#:PCAL1?' : 'Returns the first power value used for the two-point power calibration.',
    'CH#:PCAL2?' : 'Returns the second power value used for the two-point power calibration.',
    'CH#:AOUT'   : 'Description	the optical-power signal.Assigns the OUT 1 BNC port (corresponding to the # slot number) to monitor the selected signal',
    'CH#:AOUT?'  : 'Returns the parameter monitored by the OUT 1 BNC port',
    'CH#:FIRM?'  : 'Returns the software version of the module.',
    'CH#:*IDN?'  : 'Returns information about the T100 module as follows: company name, module name, serial number, software version number (FPGA version).',
    'CH#:TYPE?'  : 'Returns the T100 module type version and options.'
  
}

def lasertransmit(command_string,ser,socket):# to send command to serial device
    if not ser.is_open:
        ser.open
    ser.write(command_string)
    print(command_string)
    outputData = ser.readline()
    outputData  = outputData.decode('utf-8').strip()
    outputData = outputData.replace('\r>', '')
    socket.send(outputData)
    

def handle_client_connection(client_socket):
    while True:
        # data from PC
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break

        if data.lower() == 'quit':
            print("program end")
            break
        elif(data.lower() == 'help'):
            print("Help Information:")
            for command, description in laserHelpInformation.items():
                print(f"{command}: {description}")
        elif(data.startswith('OSCII')):
            command = (data[5:] + '\r').encode('ascii')
            lasertransmit(command,laserSerial,client_socket)
        elif(data.startswith('2')):
            #command = (userInput[1:] + '\r').encode('ascii')
            measured_current = PM32.i[0]
            client_socket.send(measured_current)

    client_socket.close()

# create socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

print("wait PC connecting...")

# 
while True:
    conn, addr = s.accept()
    print('connection IP address：', addr)
    client_thread = threading.Thread(target=handle_client_connection, args=(conn,))
    client_thread.start()
