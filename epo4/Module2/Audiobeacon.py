import serial
import time

# transmitting connection takes place over port 6
comport = 'COM6'

# getting access to bluetooth link
serial_port = serial.Serial(comport, 115200, rtscts=True)

# Audio beacon command
            serial_port.write(b'A1\n')  --on
            serial_port.write(b'A0\n') --off


            carrier_frequency = 7000.  #less than 10000 Hz
            to_bytes(2, byteorder='big')
            serial_port.write(b'F' + carrier_frequency + b'\n')

            bit_frequency = 5000.
            to_bytes(2, byteorder='big')
            serial_port.write(b'B' + bit_frequency + b'\n')

            repetition_count = 2500.
            to_bytes(2, byteorder='big')
            serial_port.write(b'R' + repetition_count + b'\n')

# close connection
serial_port.close()