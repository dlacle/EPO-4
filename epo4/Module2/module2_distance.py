import serial
import time
import re

# transmitting connection takes place over port 6
comport = 'COM6'

# getting access to bluetooth link
serial_port = serial.Serial(comport, 115200, rtscts=True)

# setting speed to neutral 155 (range 135-165)
speed = 157
fspeed = f"M{speed}\n"              # using f string for speed command

# perform the movement
serial_port.write(fspeed.encode())

for i in range(20):                 #doing 40 measurements
    time.sleep(0.2)                 #wait 0.2 second per measurement
    serial_port.write(b'Sd\n')
    numbers = re.findall(r'\d+', serial_port.read_until(b'\x04').decode()) # getting values for left and right sensort
    print(numbers)

# Shut down bluetooth connection with car
serial_port.close()