""""
This file is used for initial testing and controlling of the car
"""

import serial
import time


# Specify COMPORT of KITT
comport = 'COM7'

# Serial instance
serial_port = serial.Serial(comport, 115200, rtscts=True)

## Controlling KITT
# NEUTRAL: 150
# LEFT: 100
# RIGHT: 200
serial_port.write(b'M135\n')

# Time
time.sleep(2)

# End connection
serial_port.close()
