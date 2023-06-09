import serial
import time
import re
import numpy as np
import matplotlib.pyplot as plt

# transmitting connection takes place over port 6
comport = 'COM6'

# getting access to bluetooth link
serial_port = serial.Serial(comport, 115200, rtscts=True)

# setting speed to neutral 155 (range 135-165)
speed = int(input('driving speed: '))
fspeed = f"M{speed}\n"              # using f string for speed command

angle = int(input('driving direction: '))
fangle = f"D{angle}\n"

breaking_power = int(input('breaking_power: '))

# samples while sriving
samples = 20

# define lists
readings =[3*[]]
print(readings)