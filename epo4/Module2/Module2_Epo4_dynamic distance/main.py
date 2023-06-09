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
speed = 157
fspeed = f"M{speed}\n"              # using f string for speed command

# perform the movement
serial_port.write(fspeed.encode())

readings = [[]*2]*40

start_time = time.time()
for i in range(40):                 #doing 40 measurements
    time.sleep(0.1)                 #wait 0.1 second per measurement
    serial_port.write(b'Sd\n')
    reading = np.array(re.findall(r'\d+', serial_port.read_until(b'\x04').decode()))  # getting values for left and right sensors
    # define reading
    USL = reading[0]    #USL
    USR = reading[1]   #USR
    # print(USR)
    readings[i] = [int(USL), int(USR), time.time()-start_time]

# Shut down bluetooth connection with car
serial_port.close()

# define array of readings
readings = np.array(readings)

# Create a figure and axis object
fig,ax = plt.subplots()
axis = np.linspace(min(readings[:,2]), max(readings[:,2]), len(readings[:,2]))

# Plot the data
ax.plot(axis, readings[:, 0], c="blue", marker=".", label='USL')
ax.plot(axis, readings[:,1], c="red", marker=".", label='USR')

# Add a legend to the plot
plt.legend()

# set axis labels
plt.xlabel('time (s)')
plt.ylabel('distance (cm)')

# Show the plot
# plt.show()

# save plot as svg
plt.savefig('distance_vs_time_plot.svg')