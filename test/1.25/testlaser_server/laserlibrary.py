import time

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
    return data.decode('utf-8')

class laser(object):
    def __init__(self,socket):
            # Defaults
            self.socket = socket #IP address


    class OSICSLaser(object):

        def __init__(self, socket,channel=1):
            # Defaults
            self.socket = socket #socket connection
            self.channel = channel

        #disable CH# in laser
        def disable_channel(self,channel_number=1): 
            command = f'OSICSCH{channel_number}:DISABLE'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'OSICS Mainframe CH: {channel_number} is DISABLED')
        
        #enable CH# in laser   
        def enable_channel(self,channel_number=1): 
            command = f'OSICSCH{channel_number}:ENABLE'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'laser channel {channel_number} is ENABLED')

        #query the state of the laser-output control on the T100 module
        def query_channel_state(self,channel_number=1):
            command = f'OSICSCH{channel_number}:ENABLE?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            response = r.split(':')[1]
            if response == 'ENABLED' or response == 'DISABLED':
                print(f'laser channel {channel_number} is {response}')
        
        # Sets GHZ as the spectral unit of module
        def set_spectral_unit_GHZ(self,channel_number=1):
            command = f'OSICSCH{channel_number}:GHZ'
            send_command(command_string=command,s=self.socket)
            r = recv(self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'spectral unit for channel {channel_number} is GHZ')
        
        #Sets nm as the spectral unit of module
        def set_spectral_unit_nm(self,channel_number=1):
            command = f'OSICSCH{channel_number}:NM'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'spectral unit in channel {channel_number} is nm')

        #query the actual spectral unit
        def query_channel_spectral_unit(self,channel_number=1):
            command = f'OSICSCH{channel_number}:NM?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            response =  r.split(':')[1]
            if response == '0':
                print(f'The channel {channel_number} spectral unit is GHZ')
            elif response == '1':
                print(f'The channel {channel_number} spectral unit is nm')

        #Sets dBm as the power unit of the module
        def set_power_unit_dBm(self,channel_number=1):
            command = f'OSICSCH{channel_number}:DBM'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'power unit in channel {channel_number} is set to dBm')

        #Sets mW as the power unit of the module
        def set_power_unit_mW(self,channel_number=1):
            command = f'OSICSCH{channel_number}:MW'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'power unit in channel {channel_number} is set to mW')

        #get actual power unit
        def query_channel_power_unit(self,channel_number=1):
            command = f'OSICSCH{channel_number}:MW?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            unit = ''
            response = r.split(':')[1]
            if response == '0':
                unit = 'dBm'
            elif response == '1':
                unit = 'mW'
            print(f'The power unit of channel {channel_number} is set to {unit}')
            return unit

        #Sets the optical output-power of the module depending on the selected power unit
        def set_output_power(self,channel_number=1,value=0.00):
            command = f'OSICSCH{channel_number}:P={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The output power of channel {channel_number} is set to {value}')
            else:
                print('The value is invaild, the range is -6.99 to 11.76 (dBm)')
   

        #query output power
        def query_output_power(self,channel_number=1):
            command = f'OSICSCH{channel_number}:P?'
            unit = self.query_channel_power_unit(channel_number=channel_number)
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            output_power = r.split('=')[1]
            if output_power == 'Disabled':
                print(f'The output power of channel {channel_number} is {output_power}')
            else:
                print(f'The output power of channel {channel_number} is {output_power}{unit}')
                return float(output_power)
        
        #query the state of the output power
        def query_output_power_sate(self,channel_number=1):
            command = f'OSICSCH{channel_number}:LIMIT?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:0':
                print(f'The output power of channel {channel_number} is reached')
            elif r == f'CH{channel_number}:1':
                print(f'The output power of channel {channel_number} is not reached')
        
        #query the present current level in mA
        def query_current(self,channel_number=1):
            command = f'OSICSCH{channel_number}:I?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            current = r.split('=')[1]
            if r[-8:0] == 'Disabled':
                print(f'The optical output of channel {channel_number} is DISABLED')
            else:
                print(f'The optical output of channel {channel_number} is {current}mA')
                return float(current)
        
        #query the diode maximum current in mA
        def query_current_max(self,channel_number=1):
            command = f'OSICSCH{channel_number}:IMAX?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            max_current = r.split('=')[1]
            print(f'The maximum diode current of channel {channel_number} is {max_current}')
            return float(max_current)
        
        #Sets the emission wavelength of the module in nm
        def set_wavelength(self,channel_number=1,value=0.00):
            command = f'OSICSCH{channel_number}:L={value}'
            send_command(command_string=command,s=self.socket)
            # while True:
            #     try:
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The emission wavelength of channel {channel_number} is set to {value}nm') 
        
        #query the emission wavelength of the module in nm
        def query_wavelength(self,channel_number=1):
            command = f'OSICSCH{channel_number}:L?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            wavelength = r.split('=')[1]
            print(f'The emission wavelength of channel {channel_number} is {wavelength}nm')
            return float(wavelength)
        
        #Sets the emission frequency of the module in GHz
        def set_frequency(self,channel_number=1,value=0.00):
            command = f'OSICSCH{channel_number}:F={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The emission frequency of channel {channel_number} is set to {value}GHz')
        
        #query emission frequency of the module in GHz
        def query_frequency(self,channel_number=1):
            command = f'OSICSCH{channel_number}:F?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            frequency = r.split('=')[1]
            print(f'The frequnecy of channel {channel_number} is {frequency}GHZ')
            return float(frequency)

        #Enables/disables the Coherence Control function.
        def set_coherence_control(self,channel_number=1,opreation='OFF'):
            command = f'OSICSCH{channel_number}:CTRL {opreation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The cherence control is {opreation} in channel {channel_number}')
            else:
                print('operation error, the operation should be set OFF or ON')
        
        #query Coherence Control function
        def query_coherence_control(self,channel_number=1):
            command = f'OSICSCH{channel_number}:CTRL?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            status = 'ON' if r[-1] == '1' else 'OFF'
            print(f'The conherence control function in channel {channel_number} is {status}')
        
        #Enables/disables the Auto-peak Find function
        def set_auto_peak_find(self,channel_number=1,opreation='OFF'):
            command = f'OSICSCH{channel_number}:APF {opreation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'Auto-peak find is {opreation} in channel {channel_number}')
            else:
                print('operation error, the operation should be set OFF or ON')
        
        #query the state of the Auto-peak Find function
        def query_auto_peak_find(self,channel_number=1):
            command = f'OSICSCH{channel_number}:APF?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            status = 'ON' if r[-1] == '1' else 'OFF'
            print(f'The conherence control function in channel {channel_number} is {status}')
        
        #Sets the digital (TTL) modulation of the T100 module optical signal
        def set_TTL_modulation(self,channel_number=1,opreation= 'OFF'):
            """
            opreation has OFF,ON,ON_INV
            """
            command = f'OSICSCH{channel_number}:MOD_CTRL {opreation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'digital (TTL) modulation is {opreation} in channel {channel_number}')
            else:
                print('operation error, the operation should be set OFF,ON or ON_INV')
            
        
        #query the selected modulation activation state.
        def query_TTL_modulation_state(self,channel_number=1):
            command = f'OSICSCH{channel_number}:MOD_CTRL?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            status = r.split('=')[1]
            print(f'The conherence control function in channel {channel_number} is {status}')

        #Sets the modulation source of the T100 module
        def set_modulation_source(self,channel_number=1,source='INT'):
            """
            opreation has MAIN, INT
            """
            command = f'OSICSCH{channel_number}:MOD_SRC {source}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The modulation source was set from {source} in channel {channel_number}')
            else:
                print('operation error, the operation should be set MAIN or INT')

        #Sets the frequency of the T100 module INTERNAL digital (TTL) modulation source
        def set_TTL_modulation_frequency(self,channel_number=1,value=153):
            command = f'OSICSCH{channel_number}:MOD_F={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The frequency of the T100 module INTERNAL digital (TTL) modulation source has set to {value}Hz in channel {channel_number}')
            else:
                print('The value is invalid, the range is 153 to 1000000(1MHz)')
        
        #query the frequency selected for the internal modulation generator in Hz
        def query_internal_modulation_frequency(self,channel_number=1):
            command = f'OSICSCH{channel_number}:MOD_F?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            print(f'The frequency selected for the internal modulation generator is {r[10:]}')
        
        #query the selected modulation source
        def query_modulation_source(self,channel_number=1):
            command = f'OSICSCH{channel_number}:MOD_SRC?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            source = r.split('=')[1]
            if source == 'INT' or source == 'MAIN':
                print(f'The modulation source from {source} in channel {channel_number}')
        
        #Runs the internal wavelength referencing procedure
        def run_wavelength_ref(self,channel_number=1):
            command = f'OSICSCH{channel_number}:WAVEREF'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The internal wavelength referencing procedure finished')
        
        #Sets the wavelength value of the two-point wavelength calibration method
        def set_CAL_wavelength(self,channel_number=1,order=1,value=1490):
            command = f'OSICSCH{channel_number}:LCAL{order}={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The the NO.{order} wavelength value of the two-point wavelength calibration method in channel {channel_number} has set to {value}nm')
            else:
                print('The setting value of function set_CAL_wavelength is invaild')

        #query wavelength value of the two-point wavelength calibration method
        def query_CAL_wavelength(self,channel_number=1,order=1,value=1490):
            command = f'OSICSCH{channel_number}:LCAL{order}={value}?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            wavelength = r.split(':')[1]
            if wavelength == 'Execution Error':
                print('The setting value of function query_CAL_wavelength is invaild')
            else:
                print(f'The NO.{order} calibration wavelength of the two-point wavelength calibration method is {wavelength}nm')

        #Sets the power value of the two-point power calibration method.
        def set_CAL_power(self,channel_number=1,order=1,value=0.5):
            command = f'OSICSCH{channel_number}:PCAL{order}={value}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The the NO.{order} power value of the two-point wavelength calibration method in channel {channel_number} has set to {value}mW')
            else:
                print('The parameters of function of set_CAL_power are invalid, the order should be 1 or 2 ,the value should be range 0.3 to 0.6')

        #query calibration power value of the two-point wavelength calibration method
        def query_CAL_power(self,channel_number=1,order=1):
            command = f'OSICSCH{channel_number}:PCAL{order}?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            power = r.split('=')[1]
            print(f'The NO.{order} calibration power of the two-point wavelength calibration method is {power}mW')

        #Assigns the OUT 1 BNC port
        def assign_OUT1_BNC_port(self,channel_number=1,operation='I'):
            """
            opreation has I(current signal),P(optical power signal)
            """
            command = f'OSICSCH{channel_number}:AOUT {operation}'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:OK':
                print(f'The OUT1 BNC port of channel {channel_number} is  assigned to monitor the diodes’s {operation}')
            else:
                print('The parameters are invaild, check the channel number and the operation should be I(current signal) or P(optical power signal)')
        
        #query the parameter monitored by the OUT 1 BNC port
        def query_OUT1_BNC_port(self,channel_number=1):
            command = f'OSICSCH{channel_number}:AOUT?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:AOUT=I' or r == f'CH{channel_number}:AOUT=P':
                print(f'The {r[-1]} is monitored in channel {channel_number}')
            else:
                print('The channel number is invaild')
        
        #query Module System-Version Information
        def query_module_system_INFO(self,channel_number=1,query_info='FIRM'):
            """
            query_info has FIRM, *idn, TYPE
            """
            command = f'OSICSCH{channel_number}:{query_info}?'
            send_command(command_string=command,s=self.socket)
            r = recv(s=self.socket)
            if r == f'CH{channel_number}:Execution Error':
                print('Wrong information parameter, the query_info has FIRM, *idn, TYPE')
            else:
                print(r)