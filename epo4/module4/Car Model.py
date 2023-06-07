import numpy as np
import matplotlib.pyplot as plt

# Define Fa
def acceleration_force(Fa_max, power):
    if power >= 162 and power <=165 or (power >=135 and power < 140):
        Fa = Fa_max * (power - 150) / 15
    elif power < 162 and power >= 157:
        Fa = 4.615 + 0.8463 * (power - 158)
    elif power <= 156 and power > 155:
        Fa = 3.7687 + (power - 157) * 1.256
    elif power >=140 and power < 145:
        Fa = -6.667+(power-140)*1.333
    elif power >=135 and power < 140:
        Fa = -Fa_max/(power-135)
    else:
        Fa = 0
    return Fa

# Define function for the acceleration with respect to time
def acceleration(v, Fa, m):
    F_drag = b*np.abs(v) + c*v**2   # Drag force based on velocity using given expression
    a = 0
    if Fa >= 0 and v >= 0:
        a = (Fa - F_drag) / m               # Acceleration based on forces
    elif Fa < 0 and v <= 0:
        a = (Fa + F_drag) / m
    elif Fa < 0 and v>= 0:
        a = (Fa - F_drag) / m
    return a

def braking_force(Fb_max, power):
    Fb = Fb_max*(power-150)/15
    return Fb

def phi(steering_setting, power):
    if (steering_setting >= 150 and power >= 150) or (steering_setting <= 150 and power <= 150):
        phi = (steering_setting-150)/2
    elif (steering_setting <= 150 and power >= 150) or (steering_setting >= 150 and power <= 150):
        phi = (steering_setting - 150)/2
    return phi

# Define constants
Fa_max = 10     # Accelerating force Max.
Fb_max = 14     # Brake force Max.
b = 3.81   # Constant for linear drag force
c = 0.35  # Constant for quadratic drag force
m = 5.6     # Mass of car
L = 0.335   # Length of car

# localizing
x0 = np.array([int(input('x: '))/100, int(input('y: '))/100])   # starting location
alfa = np.radians(int(input('alfa: ')))     # staring orientation, angle of car with positive x-axis.
                                            # alfa in radians, input of alfa in degrees.
d0 = np.array([np.cos(alfa), np.sin(alfa)])     # orientation unit vector

# input car settings
power = int(input('Set motor power: ', ))
brake_power = 145
steering_setting = int(input('Set steering: ', ))
phi = phi(steering_setting, power)
print('phi: ', phi)
phi_rad = np.radians(phi)
print('phi_rad: ', phi_rad)
# estimation of R
if phi_rad != 0 and power >=150:
    R = L/np.tan(phi_rad)
elif phi_rad != 0 and power <= 150:
    R = L / np.tan(phi_rad) - L*np.tan(phi_rad)
else:
    R = 0
print('R: ', R)

# determine Fa
Fa = np.cos(phi_rad)*acceleration_force(Fa_max, power)
Fb = braking_force(Fb_max, brake_power)

# Set initial conditions
dt = 0.001   # Time step for numerical integration
drive_time = 3.5   # Final time

# Set up arrays for velocity and time
v = np.zeros(int(drive_time/dt)+1)
t = np.zeros(int(drive_time/dt)+1)

# Set initial values
driven_distance = 0

# initial speed (used for braking)
Theta = np.zeros(int((drive_time/dt)+1))
d1 = np.zeros((int((drive_time/dt)+1), 2), dtype=float)
d1[0] = d0
x1 = np.zeros((int((drive_time/dt)+1), 2), dtype=float)
x1[0] = x0
delta_Theta = np.zeros(int((drive_time/dt)+1))
t = np.zeros(int((drive_time/dt)+1))
a = np.zeros(int((drive_time/dt)+1))

# create real time figure and axis
# plt.ion()
# fig, ax = plt.subplots()
# ax.set_xlim(0,480)
# ax.set_ylim(0,480)

# Integrate forward in time
for i in range(len(v)-1):
    a[i] = acceleration(v[i], Fa, m)
    v[i+1] = v[i] + a[i]*dt
    t[i+1] = t[i] + dt

    if phi_rad != 0:
        delta_Theta[i] = (v[i] * np.sin(phi_rad) / L)
        Theta[i + 1] = (Theta[i] + delta_Theta[i] * dt)
        d1[i + 1] = [np.cos(alfa + Theta[i + 1]), np.sin(alfa + Theta[i + 1])]
        x1[i + 1] = [R*(-np.sin(alfa)+np.sin(alfa+Theta[i+1])), R*(np.cos(alfa)-np.cos(alfa+Theta[i+1]))] + x0
    else:
        delta_Theta[i] = 0
        Theta[i + 1] = (Theta[i] + delta_Theta[i] * dt)
        d1[i + 1] = d1[i]
        x1[i + 1] = x1[i]+v[i]*dt

    # time
    t[i + 1] = t[i] + dt

    # driven distance
    driven_distance = driven_distance + v[i] * dt

    # initiate brake
    if t[i+1] >= 6 and v[i+1]>0:
        Fa = Fb
    elif t[i+1] >=6 and v[i]<=0:
        Fa = 0

    # Update plot
    # plt.plot(x1[:i+1, 0], x1[:i+1, 1])  # Only update plot up to current point
    # plt.pause(dt)  # Pause to give plot time to refresh

# print(d1[int(drive_time/dt),:])
# print(x1[:,:])
# show plot
plt.plot(100*x1[:,0], 100*x1[:,1])
# plt.plot(t,v)
plt.grid(True)
plt.xlim(0,480)
plt.ylim(0,480)
# plt.xlabel('Time (s)')
# plt.ylabel('Velocity (m/s)')
# plt.title('Velocity vs. Time')
plt.show()
#
# plt.ioff()
# plot.show()
