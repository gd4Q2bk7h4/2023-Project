import time
import sys

def send_command(command_string, s):
    s.send(command_string.encode())

def recv(s):
    data_size = int(s.recv(8).decode('utf-8'))
    recv_size = 0
    data = b''
    while recv_size < data_size:
        response = s.recv(1024)
        data += response
        recv_size += len(response)
    ack = "ACK".encode()
    s.sendall(ack)
    return data.decode('utf-8')

class laser(object):
    def __init__(self,socket):
            # Defaults
            self.socket = socket #IP address

    class OSICSLaser(object):

        def __init__(self, socket,channel_number=1):
            # Defaults
            self.socket = socket #socket connection
            check_laser_avaiable = f'OSICSchannel_check:{channel_number}'
            send_command(command_string=check_laser_avaiable,s=self.socket)
            r = recv(s=self.socket)
            # print(r)
            if 'valid' in r: #match with record':
                self.channel_number = channel_number
                print('\n')
                print(r)
                print('\n')
            else:
                print('\n')
                print(r)
                print('\n')
                sys.exit(1)

        #disable CH# in laser
        def disable_channel(self): 
            command = f'OSICSCH{self.channel_number}:DISABLE'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'\nOSICS CH:{self.channel_number} is DISABLED\n')
        
        #enable CH# in laser   
        def enable_channel(self): 
            command = f'OSICSCH{self.channel_number}:ENABLE'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'\nOSICS CH:{self.channel_number} is ENABLED\n')

        #query the state of the laser-output control on the T100 module
        def query_channel_state(self):
            command = f'OSICSCH{self.channel_number}:ENABLE?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            response = r.split(':')[1]
            if response == 'ENABLED' or response == 'DISABLED':
                print(f'OSICS CH:{self.channel_number} is {response}')
        
        # Sets GHZ as the spectral unit of module
        def set_spectral_unit_GHZ(self):
            command = f'OSICSCH{self.channel_number}:GHZ'
            send_command(command_string=command,s=self.socket)
            r = recv(self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS CH:{self.channel_number} is set to GHZ')
        
        #Sets nm as the spectral unit of module
        def set_spectral_unit_nm(self):
            command = f'OSICSCH{self.channel_number}:NM'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS CH:{self.channel_number} is set to nm')

        #query the actual spectral unit
        def query_channel_spectral_unit(self):
            command = f'OSICSCH{self.channel_number}:NM?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            response =  r.split(':')[1]
            unit = ''
            if response == '0':
                print(f'OSICS CH:{self.channel_number} spectral unit is GHZ')
                unit = 'GHz'
            elif response == '1':
                print(f'OSICS CH:{self.channel_number} spectral unit is nm')
                unit = 'nm'
            return unit

        #Sets dBm as the power unit of the module
        def set_power_unit_dBm(self):
            command = f'OSICSCH{self.channel_number}:DBM'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS CH:{self.channel_number} is set to dBm')

        #Sets mW as the power unit of the module
        def set_power_unit_mW(self):
            command = f'OSICSCH{self.channel_number}:MW'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS CH:{self.channel_number} is set to mW')

        #get actual power unit
        def query_channel_power_unit(self):
            command = f'OSICSCH{self.channel_number}:MW?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            unit = ''
            response = r.split(':')[1]
            if response == '0':
                unit = 'dBm'
            elif response == '1':
                unit = 'mW'
            print(f'OSICS CH:{self.channel_number} is set to {unit}')
            return unit

        #Sets the optical output-power of the module depending on the selected power unit
        def set_output_power(self,value=0.00):
            command = f'OSICSCH{self.channel_number}:P={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS CH:{self.channel_number} is set to {value} dBm')
            else:
                print('OSICS Mainframe: The output_power value setting is invaild, the range is -6.99 to 11.76 (dBm)')

        #query output power
        def query_output_power(self):
            command = f'OSICSCH{self.channel_number}:P?'
            unit = self.query_channel_power_unit(self)
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            output_power = r.split('=')[1]
            if output_power == 'Disabled':
                print(f'OSICS CH:{self.channel_number} set to {output_power}')
            else:
                print(f'OSICS CH:{self.channel_number} set to {output_power} {unit}')
                return float(output_power)

        #query the state of the output power
        def query_output_power_sate(self):
            command = f'OSICSCH{self.channel_number}:LIMIT?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:0':
                print(f'OSICS CH:{self.channel_number} has reached set power')
            elif r == f'CH{self.channel_number}:1':
                print(f'OSICS CH:{self.channel_number} has not reached set power')

        #query the present current level in mA
        def query_current(self):
            command = f'OSICSCH{self.channel_number}:I?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            current = r.split('=')[1]
            if r[-8:0] == 'Disabled':
                print(f'OSICS Mainframe: The optical output of channel {self.channel_number} is DISABLED')
            else:
                print(f'OSICS Mainframe: The optical output of channel {self.channel_number} is {current}mA')
                return float(current)

        #query the diode maximum current in mA
        def query_current_max(self):
            command = f'OSICSCH{self.channel_number}:IMAX?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            max_current = r.split('=')[1]
            print(f'OSICS Mainframe: The maximum diode current of channel {self.channel_number} is {max_current}')
            return float(max_current)

        #Sets the emission wavelength of the module in nm
        def set_wavelength(self,value=0.00):
            command = f'OSICSCH{self.channel_number}:L={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS CH:{self.channel_number} is set to {value} nm')
            else:
                print(f'OSICS Mainframe:The wavelength value setting is invalid, the range is 1490 to 1680 (nm)')

        #query the emission wavelength of the module in nm
        def query_wavelength(self):
            command = f'OSICSCH{self.channel_number}:L?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            wavelength = r.split('=')[1]
            print(f'OSICS CH:{self.channel_number} is {wavelength} nm')
            return float(wavelength)

        #Sets the emission frequency of the module in GHz
        def set_frequency(self,value=0.00):
            command = f'OSICSCH{self.channel_number}:F={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS CH:{self.channel_number} is set to {value} GHz')
            else:
                print(f'OSICS Mainframe:The frequency value setting is invalid')

        #query emission frequency of the module in GHz
        def query_frequency(self):
            command = f'OSICSCH{self.channel_number}:F?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            frequency = r.split('=')[1]
            print(f'OSICS CH:{self.channel_number} is {frequency} GHZ')
            return float(frequency)

        #Enables/disables the Coherence Control function.
        def set_coherence_control(self,opreation='OFF'):
            command = f'OSICSCH{self.channel_number}:CTRL {opreation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS Mainframe: The cherence control is {opreation} in channel {self.channel_number}')
            else:
                print('OSICS Mainframe: operation error, the operation should be set OFF or ON')

        #query Coherence Control function
        def query_coherence_control(self):
            command = f'OSICSCH{self.channel_number}:CTRL?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            status = 'ON' if r[-1] == '1' else 'OFF'
            print(f'OSICS Mainframe: The conherence control function in channel {self.channel_number} is {status}')

        #Enables/disables the Auto-peak Find function
        def set_auto_peak_find(self,opreation='OFF'):
            command = f'OSICSCH{self.channel_number}:APF {opreation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS Mainframe: Auto-peak find is {opreation} in channel {self.channel_number}')
            else:
                print('OSICS Mainframe: operation error, the operation should be set OFF or ON')

        #query the state of the Auto-peak Find function
        def query_auto_peak_find(self):
            command = f'OSICSCH{self.channel_number}:APF?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            status = 'ON' if r[-1] == '1' else 'OFF'
            print(f'OSICS Mainframe: The conherence control function in channel {self.channel_number} is {status}')

        #Sets the digital (TTL) modulation of the T100 module optical signal
        def set_TTL_modulation(self,opreation= 'OFF'):
            """
            opreation has OFF,ON,ON_INV
            """
            command = f'OSICSCH{self.channel_number}:MOD_CTRL {opreation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS Mainframe: digital (TTL) modulation is {opreation} in channel {self.channel_number}')
            else:
                print('OSICS Mainframe: operation error, the operation should be set OFF,ON or ON_INV')
            
        
        #query the selected modulation activation state.
        def query_TTL_modulation_state(self):
            command = f'OSICSCH{self.channel_number}:MOD_CTRL?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            status = r.split('=')[1]
            print(f'OSICS Mainframe: The conherence control function in channel {self.channel_number} is {status}')

        #Sets the modulation source of the T100 module
        def set_modulation_source(self,source='INT'):
            """
            opreation has MAIN, INT
            """
            command = f'OSICSCH{self.channel_number}:MOD_SRC {source}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS Mainframe: The modulation source was set from {source} in channel {self.channel_number}')
            else:
                print('OSICS Mainframe: operation error, the operation should be set MAIN or INT')

        #Sets the frequency of the T100 module INTERNAL digital (TTL) modulation source
        def set_TTL_modulation_frequency(self,value=153):
            command = f'OSICSCH{self.channel_number}:MOD_F={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS Mainframe: The frequency of the T100 module INTERNAL digital (TTL) modulation source has set to {value}Hz in channel {self.channel_number}')
            else:
                print('OSICS Mainframe: The value is invalid, the range is 153 to 1000000(1MHz)')
        
        #query the frequency selected for the internal modulation generator in Hz
        def query_internal_modulation_frequency(self):
            command = f'OSICSCH{self.channel_number}:MOD_F?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            print(f'OSICS Mainframe: The frequency selected for the internal modulation generator is {r[10:]}')
        
        #query the selected modulation source
        def query_modulation_source(self):
            command = f'OSICSCH{self.channel_number}:MOD_SRC?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            source = r.split('=')[1]
            if source == 'INT' or source == 'MAIN':
                print(f'OSICS Mainframe: The modulation source from {source} in channel {self.channel_number}')
        
        #Runs the internal wavelength referencing procedure
        def run_wavelength_ref(self):
            command = f'OSICSCH{self.channel_number}:WAVEREF'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS Mainframe: The internal wavelength referencing procedure finished')

        #Assigns the OUT 1 BNC port
        def assign_OUT1_BNC_port(self,operation='I'):
            """
            opreation has I(current signal),P(optical power signal)
            """
            command = f'OSICSCH{self.channel_number}:AOUT {operation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:OK':
                print(f'OSICS Mainframe:The OUT1 BNC port of channel {self.channel_number} is  assigned to monitor the diodes’s {operation}')
            else:
                print('OSICS Mainframe:The parameters are invaild, check the channel number and the operation should be I(current signal) or P(optical power signal)')

        #query the parameter monitored by the OUT 1 BNC port
        def query_OUT1_BNC_port(self):
            command = f'OSICSCH{self.channel_number}:AOUT?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:AOUT=I' or r == f'CH{self.channel_number}:AOUT=P':
                print(f'OSICS Mainframe: The {r[-1]} is monitored in channel {self.channel_number}')
            else:
                print('OSICS Mainframe: The channel number is invaild')

        #query Module System-Version Information
        def query_module_system_INFO(self,query_info='FIRM'):
            """
            query_info has FIRM, *idn, TYPE
            """
            command = f'OSICSCH{self.channel_number}:{query_info}?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{self.channel_number}:Execution Error':
                print('OSICS Mainframe: Wrong information parameter, the query_info has FIRM, *idn, TYPE')
            else:
                print(f'OSICS Mainframe: {r}')