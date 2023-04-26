""""
This file is used for initial testing and controlling of the car
"""

import serial
import time


# Specify COMPORT of KITT
comport = 'COM7'

# Serial instance
serial_port = serial.Serial(comport, 115200, rtscts=True)

# Controlling KITT
# neutral: 150
# Hard left: 100
# Hard right: 200
# Backward: 135
# Forward: 165
serial_port.write(b'M153\n')

# Time loop in seconds
time.sleep(2)

# End connection
serial_port.close()
