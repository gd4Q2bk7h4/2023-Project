from __future__ import print_function
import serial, re, time
import vxi11	# pip install python-vxi11==0.9

class Quantifi(object):
	"""
	Super class which handles serial communication, device identification, and logging with a Quantifi laser.

	ip_address = None
                  192.168.101.201
	"""

	response_timeout = 0.200  # Timeout for RESPONSE_OK or error to set commands

	def __init__(self, ip_addr):
		"""
		Constructor.
		"""
		self.ip_address = ip_addr

		try:
			self.laser = vxi11.Instrument(self.ip_address)
		except:
			raise AttributeError("No device found on ip_address: {}".format(self.ip_address))

		self.init_time = time.time()
		print('\nConnected to Quantifi laser on ip address: {0}\n'.format(self.ip_address))

	def close(self):
		"""
		Destructor.
		"""
		self.laser.close()

	def transmit(self, command_string):
		"""
		Low-level transmit data method.
		"""
		self.laser.write(command_string)

	def query(self, command_string):
		return self.laser.ask(command_string)

	def identify(self):
		print(self.query('*IDN?'))

	def operation_complete_query(self):
		state = int(self.query('*OPC?'))
		if state == 0:
			# print('Laser Busy...')
			return 'busy'
		elif state == 1:
			# print('Laser not busy')
			return 'not_busy'
		else:
			print('Error: ' + state)

	def get_laser_wavelength(self):
		"""
		Queries the current wavelength of the laser in nm
		"""
		wavelength = round((float(self.query('SOUR1:CHAN1:WAV? ACT')) * 1e9), 4)
		return wavelength
	
	def laser_wavelength_query(self):
		"""
		Queries whether the laser has reached the set wavelength
		Returns TRUE or FALSE
		"""
		wavelength = self.query('SOUR1:CHAN1:WAV? LOCK')
		return wavelength

	def set_laser_wavelength(self, wavelength):
		wavelength_m = round((wavelength * 1e-09), 14)
		if (wavelength > 1527.60488)and (wavelength < 1568.77267):
			print(wavelength_m)
			self.transmit('SOUR1:CHAN1:WAV {}'.format(wavelength_m))
			current_wavelength = float(self.get_laser_wavelength())
			print(current_wavelength)
			while current_wavelength != float(wavelength):
				time.sleep(0.1)
				current_wavelength = float(self.get_laser_wavelength())
			ready = self.operation_complete_query()
			while ready == 'busy':
				time.sleep(0.1)
				ready = self.operation_complete_query()
			print('Wavelength set to: {}'.format(round((float(self.query('SOUR1:CHAN1:WAV?')) * 1e9), 4)))
		elif wavelength < 1527.60488:
			print('Wavelength set too small!\nMin wavelength: 1527.7 nm\nMax wavelength: 1568.7 nm\nSet wavelength: {: 4.1f} nm'.format(wavelength))
		elif wavelength > 1568.77267:
			print('Wavelength set too large!\nMin wavelength: 1527.7 nm\nMax wavelength: 1568.7 nm\nSet wavelength: {: 4.1f} nm'.format(wavelength))
		else:
			print('Incorrect wavelength setting!\nMin wavelength: 1527.7 nm\nMax wavelength: 1568.7 nm\nSet wavelength: {: 4.1f} nm'.format(wavelength))


	def switch_on(self):
		self.transmit('OUTP1:CHAN1:STATE ON')
		print('Laser ENABLED')

	def switch_off(self):
		self.transmit('OUTP1:CHAN1:STATE OFF')
		print('Laser DISABLED')

	def get_laser_power(self):
		return self.query('SOUR1:CHAN1:POW?')
	
	def get_laser_temperature(self):
		return self.query('SOUR1:CHAN1:TEMP?')
		
	def set_laser_power(self, power):
		if (power > 7.5) and (power < 16.5):
			self.transmit('SOUR1:CHAN1:POW {: 2.2f}'.format(power))
			current_power = float(self.get_laser_power())
			while current_power != power:
				time.sleep(0.1)
				current_power = float(self.get_laser_power())
			ready = self.operation_complete_query()
			while ready == 'busy':
				time.sleep(0.1)
				ready = self.operation_complete_query()
			print('Laser power set to: {}'.format(self.get_laser_power()))
		elif power < 7.5:
			print('Power set too low!\nMin power: 7.5 dBm\nMax power: 16.5 dBm\nSet power: {: 2.2f} dBm'.format(power))
		elif power < 7.5:
			print('Power set too high!\nMin power: 7.5 dBm\nMax power: 16.5 dBm\nSet power: {: 2.2f} dBm'.format(power))
		else:
			print('Incorrect power setting!\nMin power: 7.5 dBm\nMax power: 16.5 dBm\nSet power: {: 2.2f} dBm'.format(power))

	def get_laser_state(self):
		state = self.query('OUTP1:CHAN1:STATE?')
		if state == 'ON':
			#print("ENABLED")
			return "ENABLED"
		elif state == 'OFF':
			#print("DISABLED")
			return "DISABLED"
		else:
			pass
