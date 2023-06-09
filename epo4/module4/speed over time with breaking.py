import serial
import time
import re
import numpy as np
import matplotlib.pyplot as plt
import csv

# transmitting connection takes place over port 6
comport = 'COM6'

# getting access to bluetooth link
serial_port = serial.Serial(comport, 115200, rtscts=True)

# setting speed to neutral 155 (range 135-165)
speed = int(input('driving speed: '))
fspeed = f"M{speed}\n"              # using f string for speed command

angle = int(input('driving direction: '))
fangle = f"D{angle}\n"

breaking_power = int(input('breaking power: '))
#set straight
serial_port.write(fangle.encode())

# amount of samples
samples = 20

readings = [[]*2]*samples
Distance = []
Time = []
mspeed = np.zeros(samples)
T = np.zeros(samples)
s = np.zeros(samples)

def func_speed(s, T):
    v = s/T
    return v

start_time = time.time()
for i in range(samples):                 #doing 40 measurements
    time.sleep(0.07)                     #wait 0.1 second per measurement
    # perform the movement
    serial_port.write(fspeed.encode())

    serial_port.write(b'Sd\n')
    reading = np.array(re.findall(r'\d+', serial_port.read_until(b'\x04').decode()))  # getting values for left and right sensors
    # define reading
    USL = reading[0]    #USL
    USR = reading[1]    #USR
    # print(USR)
    readings[i] = [int(USL), int(USR), time.time()-start_time]

    # average distance measured by the 2 sensors put in a array
    Distance.append(((np.array(readings[i])[0])+(np.array(readings[i])[1]))/2)

    # Time of measurement put in an array
    Time.append(np.array(readings[i])[2])

    # determining the average speed over time interval T in meters/second
    if i>4:
        s[i] = -(Distance[i] - Distance[i - 5]) / 100
        T[i] = Time[i] - Time[i - 5]
        v = func_speed(s[i], T[i])
        mspeed[i] = v

    # initiating break
    if i>(2*samples/3) and mspeed[i]>0 and speed != 150:
        speed = breaking_power
        fspeed = f"M{speed}\n"
    elif i>(2*samples/3) and mspeed[i]<=0 and speed != 150:
        speed = 150
        fspeed = f"M{speed}\n"
    elif Time[i] >= 1 and mspeed[i] >= 1:
        speed = 158
        fspeed = f"M{speed}\n"

# arrays
mspeed = np.array(mspeed)
readings = np.array(readings)
Distance = np.array(Distance)
T = np.array(T)
s = np.array(s)
print(Time[samples-1])
# Shut down bluetooth connection with car
serial_port.close()

# define array of readings
readings = np.array(readings)

# Create a figure and axis object
fig,ax = plt.subplots()
speed_flat = mspeed.flatten()
axis = np.linspace(min(readings[4:,2]), max(readings[4:,2]), len(readings[4:,2]))

# Plot the data
ax.plot(axis, speed_flat[4:], c="blue", marker="", label='speed')
# ax.plot(axis, Distance, c="red", marker="", label='USR')
# ax.plot(axis, readings[:,0]/100, c="green", marker="", label='USL')

# Add a legend to the plot
plt.legend()

# set axis labels
plt.xlabel('time (s)')
plt.ylabel('speed (m/s)')

# Show the plot
# plt.show()

# save plot as svg
plt.savefig('distance_vs_time_plot(speed165160)_nobreak.svg')

# save data
data = list(zip(mspeed, readings[:, 2], Distance, T, s))
with open('data_speed165160_nobreak', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['mspeed', 'readings', 'Distance', 'T', 's'])
    writer.writerows(data)