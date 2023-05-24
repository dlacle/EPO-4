import serial
import time
import re
import numpy as np
import matplotlib.pyplot as plt

# setting speed to neutral 155 (range 135-165)
speed = int(input('begin speed: ', ))
fspeed = f"M{speed}\n"              # using f string for speed command

angle = int(input('begin angle: ', ))
fangle = f"D{angle}\n"

speed_steps = int(input('speed_steps: ',))
angle_steps = int(input('angle_steps: ',))

# amount of samples per setting
samples = 3

readings = [[]*2]*samples

def func_speed(s, T):
    v = s/T
    return v

start_time = time.time()
while speed > 144 and speed <= 165 and angle >=100 and angle <=200:
    print('fangle: ', fangle) #angle encode/write
    print('fspeed: ', fspeed)#speed encode/write
    for i in range(samples):                 #doing 40 measurements
        print('speed: ', speed)
        print('angle: ', angle)
        # doing measurements on current settings

    # stop driving for x sec

    speed += speed_steps
    fspeed = f"D{speed}\n"
    angle += angle_steps
    fangle = f"D{angle}\n"
