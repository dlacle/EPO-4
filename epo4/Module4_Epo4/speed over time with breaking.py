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

breaking_power = int(input('breaking power: '))
#set straight
serial_port.write(fangle.encode())

# amount of samples
samples = 60

readings = [[]*2]*samples
Distance = []
Time = []
mspeed = np.zeros(samples)

def func_speed(s, T):
    v = s/T
    return v

def moving_average(data, window_size):
    window =np.ones(int(window_size))/float(window_size)
    return np.convolve(data, window, 'same')

def break_car(breaking_power):
    speed = breaking_power
    return(speed)

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
    print(Distance)

    # Time of measurement put in an array
    Time.append(np.array(readings[i])[2])
    print(Time)

    # determining the average speed over time interval T in meters/second
    if i>0:
        s = -(Distance[i] - Distance[i - 1]) / 100
        T = Time[i] - Time[i - 1]
        v = func_speed(s, T)
        mspeed[i] = v
    else:
        v = 0
        mspeed[i] = v

    if i>(2*samples/3) and mspeed[i]>0 and speed != 150:
        speed = breaking_power
        fspeed = f"M{speed}\n"
    elif i>(2*samples/3) and mspeed[i]<=0 and speed != 150:
        speed = 150
        fspeed = f"M{speed}\n"

# array of speed
mspeed = np.array(mspeed)
readings = np.array(readings)

print(mspeed)

# Shut down bluetooth connection with car
serial_port.close()

# define array of readings
readings = np.array(readings)

moving_average(mspeed, 4)
# Create a figure and axis object
fig,ax = plt.subplots()
speed_flat = mspeed.flatten()
axis = np.linspace(min(readings[:,2]), max(readings[:,2]), len(readings[:,2]))

# Plot the data
ax.plot(axis, speed_flat, c="blue", marker="", label='speed')
ax.plot(axis, readings[:,1]/100, c="red", marker="", label='USR')
ax.plot(axis, readings[:,0]/100, c="green", marker="", label='USL')

# Add a legend to the plot
plt.legend()

# set axis labels
plt.xlabel('time (s)')
plt.ylabel('distance (cm)')

# Show the plot
plt.show()

# # save plot as svg
plt.savefig('distance_vs_time_plot(speed165).svg')