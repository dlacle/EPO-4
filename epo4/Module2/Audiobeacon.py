import time

import serial

# transmitting connection takes place over port 6
comport = 'COM7'

# getting access to bluetooth link
serial_port = serial.Serial(comport, 115200, rtscts=True)


# Audio beacon command
serial_port.write(b'A1\n')  # on


# Carrier freq = 20 kHz
carrier_frequency = (15000).to_bytes(2, byteorder='big')
serial_port.write(b'F' + carrier_frequency + b'\n')

# Bit freq = 5 kHz
bit_frequency = (1000).to_bytes(2, byteorder='big')
serial_port.write(b'B' + bit_frequency + b'\n')

# Repetition count = bit freq / repetition freq
repetition_count = (10).to_bytes(2, byteorder='big')
serial_port.write(b'R' + repetition_count + b'\n')

code = 0xDEADBEEF.to_bytes(4, byteorder='big')
serial_port.write(b'C' + code + b'\n')
time.sleep(10)

serial_port.write(b'A0\n')  # off
time.sleep(1)
# close connection
serial_port.close()
