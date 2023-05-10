"""
Audio beacon and code transmission of Module 2
"""

import time
import serial

# transmitting connection takes place over port 7
comport = 'COM7'

# getting access to bluetooth link
try:
    serial_port = serial.Serial(comport, 115200, rtscts=True)
except serial.SerialException as var :
    print("Error has occured")
    print("var")
else
    print("serial port opened")


# Audio beacon command
serial_port.write(b'A1\n')  # on

# Carrier freq = 7 kHz
carrier_frequency = (7000).to_bytes(2, byteorder='big')
serial_port.write(b'F' + carrier_frequency + b'\n')

# Bit freq = 5 kHz
bit_frequency = (2000).to_bytes(2, byteorder='big')
serial_port.write(b'B' + bit_frequency + b'\n')

# Repetition count = bit freq / repetition freq
repetition_count = (1250).to_bytes(2, byteorder='big')
serial_port.write(b'R' + repetition_count + b'\n')

# Gold code
code = 0x3355A780.to_bytes(4, byteorder='big')
serial_port.write(b'C' + code + b'\n')
time.sleep(10)

serial_port.write(b'A0\n')  # off

# close connection
serial_port.close()
