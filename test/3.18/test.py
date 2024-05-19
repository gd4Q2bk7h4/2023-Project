import laser_test
ip_addr = '192.168.101.201'
laser = laser_test.Quantifi(ip_addr= ip_addr)

laser.switch_on()
laser.switch_off()
laser.set_laser_wavelength(1528)