# # This is a sample Python script.
# import time
# import csv
# # Press ⌃R to execute it or replace it with your code.
# # Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# from pathlib import Path
# import math
# import sympy as sp
# from sympy.abc import s
# import control
# import time
# import re
# import numpy as np
# from scipy import stats
# from numpy.random import seed
# from numpy.random import randn
# from numpy.random import normal
# from scipy import stats
# import pandas as pd
#
# import matplotlib.pyplot as plt
# def moving_average(data, window_size):
#     window = np.ones(int(window_size))/float(window_size)
#     return np.convolve(data, window, 'same')
#
#
# t = range(1, 35)
#
# n= np.arange(0,20)
#
# L=[28,
# 31,
# 24,
# 26,
# 30,
# 35,
# 40,
# 45,
# 50,
# 55,
# 60,
# 65,
# 71,
# 75,
# 80,
# 85,
# 90,
# 95,
# 100,
# 110,
# 121,
# 130,
# 140,
# 150,
# 160,
# 170,
# 180,
# 190,
# 200,
# 210,
# 222,
# 230,
# 240,
# 250]
# R=[26,
# 31,
# 24,
# 26,
# 30,
# 36,
# 40,
# 45,
# 50,
# 55,
# 61,
# 66,
# 71,
# 75,
# 80,
# 85,
# 91,
# 95,
# 100,
# 111,
# 120,
# 130,
# 139,
# 150,
# 160,
# 170,
# 197,
# 189,
# 200,
# 210,
# 220,
# 229,
# 238,
# 249]
# M=[10,
# 15,
# 20,
# 25,
# 30,
# 35,
# 40,
# 45,
# 50,
# 55,
# 60,
# 65,
# 70,
# 75,
# 80,
# 85,
# 90,
# 95,
# 100,
# 110,
# 120,
# 130,
# 140,
# 150,
# 160,
# 170,
# 180,
# 190,
# 200,
# 210,
# 220,
# 230,
# 240,
# 250]
# dyM=[[201, 199],
# [200, 199],
# [198, 197],
# [194, 194],
# [189, 190],
# [184, 181],
# [178, 174],
# [165, 168],
# [157, 161],
# [149, 145],
# [141, 136],
# [122, 128],
# [112, 118],
# [102, 98],
# [92, 88],
# [81, 78],
# [59, 67],
# [48, 45],
# [37, 34],
# [26, 23]]
# dy=np.array(dyM)
#
# E=np.array(dy[:,0])-np.array(dy[:,1])
# E1=np.array(M)-np.array(L)
# #print(dy.shape)
# z = dy[:,0]
# #print(z)
#
#
# fig = plt.figure()
# # ax = plt.axes()
# # plt.xlabel("Time (sec)")
# # plt.ylabel("Distance (cm)")
# # ax.plot(n, dy[:,0],'--k',label='L sensor')
# # ax.plot(n, dy[:,1],'r--',label='R sensor')
# # ax.plot(n,(dy[:,0]+dy[:,1])/2,label='Average L & R')
# # plt.legend()
#
# #ax.plot(t,L)
# #ax.plot(t, M)
# #ax.plot(t)
#
# plt.show()
# fn = Path('~/Documents/avgsensor.svg').expanduser()
# fig.savefig(fn, bbox_inches='tight')
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
# import control
# import sympy
# from sympy import symbols
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.integrate import odeint
#
# # System parameters
# m = 5.6                # mass of the object
# b = 5                # spring constant
# c = 0.1                # damping coefficient
# F=5.5
# def force_func(x, v):
#     """Returns the force acting on the object at position x and velocity v."""
#     return F-math.copysign(1, F)*(b*abs(v)+c*v**2)
#
# def derivatives(y, t):
#     """Returns the derivatives of the position and the velocity at time t."""
#     x, v = y
#     dx_dt = v
#     dv_dt = force_func(x, v) / m
#     return [dx_dt, dv_dt]
#
# # Initial conditions
#
# y0 = [0.0, 0.0]        # initial position and velocity
# t = np.linspace(0, 8, 80)    # time points to evaluate at
# start=time.time()
# # Solve the differential equations
# y = odeint(derivatives, y0, t)
# end=time.time()
# print(end - start)
# #Plot the solutions
# fig = plt.figure()
# plt.plot(t, y[:, 0], label='position')
# plt.plot(t, y[:, 1], label='velocity')
# plt.legend()
# plt.xlabel('time')
# plt.ylabel('position/velocity')
# plt.show()
#
# fn = Path('~/Documents/model.svg').expanduser()
# fig.savefig(fn, bbox_inches='tight')
#
#
# speed = []
# readings = []
# distance = []
#
#
# from scipy.signal import savgol_filter
#
# #
# # x = np.linspace(0,2*np.pi,100)
# # y = np.sin(x) + np.random.random(100) * 0.2
# # yhat = savgol_filter(y, 51, 3) # window size 51, polynomial order 3
# #
# # plt.plot(x,y)
# # plt.plot(x,yhat, color='red')
# # plt.show()
#
#
#
#
#
# with open('data_speed165_break145.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     next(reader)  # skip the header row
#     for row in reader:
#         speed.append(row[0])
#         readings.append(row[1])
#         distance.append(row[2])
# speed = np.array(speed)
# readings = np.array(readings)
# print(len(readings))
# distance = np.array(distance)
#
# print(speed)
# speed=np.array(speed)
# print(type(readings))
# print(max(readings))
# fig = plt.figure()
# axis = np.linspace(0, 1, len(readings))
# speed_flat = speed.flatten()
# # Plot the data
# plt.fig(axis, speed, c="blue", marker="", label='speed')
# #ax.plot(axis, readings/100, c="red", marker="", label='USR')
# #ax.plot(axis, readings/100, c="green", marker="", label='USL')
# plt.legend()
# plt.show()

import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import keyboard


def deg_to_pwm(angle):
    pwm_value = round(((angle + 25) / 50) * (MAX_PWM - MIN_PWM) + MIN_PWM)
    if pwm_value > 200:
        pwm_value = 200
    elif pwm_value < 100:
        pwm_value = 100
    return pwm_value


# dt, t = set_time(start_time, t)
def set_time(start, last_time):
    interval = time.time() - last_time - start
    T = time.time() - start
    return interval, T


# relative location of end location x1
def relative_loc(x0, x1, alpha):
    dx_vector = np.array([x1[0] - x0[0], x1[1] - x0[1]])  # distance/direction vector between location 0 and 1
    dx = np.linalg.norm(dx_vector)  # distance to location 1
    angle_beta = beta(x0[0], x0[1], x1[0], x1[1])  # angle between dx_vector and positive x-axis
    omega = angle_beta - alpha  # angle between dx_vector and d0
    omega = call_angle(omega)
    return dx, omega


# measure location according to the car model
# dt, t, v, x0, d0, alpha = measure_loc(dt, t, v, m, Turn, L, alpha, power, x0, Fa_max)
def measure_loc(t, v_old, m, Turn, L, alpha, power, old_x0, fa_max):
    DT, T = set_time(start_time, t)
    PHI = phi(Turn, phi_max)
    phi_rad = np.radians(PHI)
    phi_rad = call_angle(phi_rad)
    Fa = np.cos(phi_rad) * acceleration_force(fa_max, power)
    a = acceleration(v_old, Fa, m)
    v = v_old + a * DT

    if phi_rad != 0:  # if the car turns
        R = radius(phi_rad, v)
        delta_theta = (v * np.sin(phi_rad) / L)
        theta = (delta_theta * DT)
        d_new = np.array([np.cos(alpha + theta), np.sin(alpha + theta)])
        x_new = np.array([R * (-np.sin(alpha) + np.sin(alpha + theta)),
                          R * (np.cos(alpha) - np.cos(alpha + theta))]) + old_x0
    else:  # if the car drives straight
        d_new = np.array([np.cos(alpha), np.sin(alpha)])
        x_new = old_x0 + v * DT * d_new
        theta = 0

    X0 = x_new
    D0 = d_new
    Alpha = alpha + theta
    Alpha = call_angle(Alpha)
    return DT, T, v, X0, D0, Alpha


# Define radius
def radius(phi_rad, speed):
    # estimation of R
    if phi_rad != 0 and speed > 0:
        R = L / np.sin(phi_rad)  # radius driving forward
    elif phi_rad != 0 and speed < 0:
        R = L / np.tan(phi_rad)
    else:
        R = 0
    return R


# Define Fa (based on Fa_max=10) and measurements
def acceleration_force(Fa_max, power):
    if power >= 162 and power <= 165 or (power >= 135 and power < 140):
        Fa = Fa_max * (power - 150) / 15
    elif power < 162 and power >= 157:
        Fa = Fa_max * (4.615 + 0.8463 * (power - 158)) / 10
    elif power <= 156 and power > 155:
        Fa = Fa_max * (3.7687 + (power - 157) * 1.256) / 10
    elif power >= 140 and power < 145:
        Fa = Fa_max * (-6.667 + (power - 140) * 1.333) / 10
    elif power >= 135 and power < 140:
        Fa = -Fa_max / (power - 135)
    else:
        Fa = 0
    return Fa


# Define function for the acceleration with respect to time
def acceleration(v, Fa, m):
    f_drag = b * np.abs(v) + c * pow(v, 2)  # Drag force based on velocity using given expression
    if Fa >= 0 and v >= 0:
        a = (Fa - f_drag) / m  # Acceleration based on forces
    elif Fa >= 0 and v < 0:
        a = (Fa + f_drag) / m
    elif Fa < 0 and v <= 0:
        a = (Fa + f_drag) / m
    elif Fa < 0 and v >= 0:
        a = (Fa - f_drag) / m
    else:
        a = 0
    return a


def braking_force(Fb_max, power):
    Fb = Fb_max * (power - 150) / 15
    return Fb


def phi(steering_setting, phi_max):
    # if steering_setting > 150:
    Phi = phi_max * (steering_setting - 150) / 50
    # elif steering_setting < 150:
    #     Phi = phi_max*(steering_setting - 150)/2
    # else:
    #     Phi = 0
    return Phi


# determining location x1 with respect to x0
def beta(x0, y0, x1, y1):
    dx = np.array([x1 - x0, y1 - y0])  # distance/direction vector between location 0 and 1
    angle_beta = np.arctan2(dx[1], dx[0])  # angle of dx vector with positive x-axis (requested direction)
    angle_beta = call_angle(angle_beta)
    return angle_beta


# set angle in range -pi to pi
def call_angle(angle):
    angle = angle % (2 * np.pi)
    if angle > np.pi:
        angle = angle - 2 * np.pi
    return angle


class KITT:
    def __init__(self, comport):  # called when the class is used to create a new object
        self.serial = serial.Serial(comport, baudrate=115200, rtscts=True)

    def set_speed(self, speed):
        fspeed = f"M{speed}\n"
        self.serial.write(fspeed.encode())

    def set_angle(self, angle):
        fangle = f"D{angle}\n"
        self.serial.write(fangle.encode())

    def stop(self):
        power = 150
        turn = 150
        self.set_angle(turn)
        self.set_speed(power)
        return power, turn

    def brake(self, speed):
        brake_power = (np.abs(speed) / speed) * 5 + 150
        brake_time = np.abs(speed / 2.3)
        start = time.time()
        T = 0
        while T <= brake_time:
            self.set_speed(brake_power)
            T = T + time.time() - start

    def drive(self, power, turn):
        self.set_angle(turn)
        self.set_speed(power)

    def __del__(self):
        self.serial.close()


# Define constants
# Fa_max = 10.615                 # Accelerating force Max.
Fb_max = 17.7  # Brake force Max.
b = 0.75  # Constant for linear drag force
c = 1.5  # Constant for quadratic drag force
Fa_max0 = b * 2.3 + c * pow(2.3, 2)  # Accelerating force Max.
Fa_max = Fa_max0
m = 5.6  # Mass of car
L = 0.335  # Length of car
phi_max = 28  # Max. steering angle

# limit conditions
R_min_forward = radius(np.radians(phi_max), 1)
R_min_backward = radius(np.radians(phi_max), -1)

MIN_PWM = 100
MAX_PWM = 200

# transmitting connection takes place over port 6
comport = 'COM8'
# kitt = KITT(comport)                                                    # create KITT object

# determine begin and end location
x0 = np.array([int(input('x0: ', )) / 100, int(input('y0: ', )) / 100])  # [x0,y0] starting location
alpha = np.radians(int(input('starting orientaion: ', )))  # starting orientation angle with x-axis
d0 = np.array([np.cos(alpha), np.sin(alpha)])  # starting orientation vector
x1 = np.array([int(input('x1: ', )) / 100, int(input('y1: ', )) / 100])  # [x1, y1] end location
x2 = np.array([int(input('x2: ', )) / 100, int(input('y2: ', )) / 100])  # [x1, y1] end location

# initial values
v = 0
start_time = time.time()
dt, t = set_time(start_time, 0)
Fa = 0

# plot starting and end location
plt.plot(x0[0], x0[1], marker='o')
plt.plot(x1[0], x1[0], marker='o')
plt.plot(x2[0], x2[1], marker='o')

x_target = x1

dx, omega = relative_loc(x0, x_target, alpha)  # update end location relative to car location

# drive from point to point
while dx > 0.001:
    time.sleep(0.01)

    if x0[0] < 0.25 or x0[0] > 4.55 or x0[1] < 0.25 or x0[1] > 4.55:
        power = 142  # backward
        turn = 150  # straight (but slightly turning against off-set, only noticeable when driving backward)
        # kitt.drive(power, turn)
        dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)
    elif dx < np.abs(np.sin(omega) * 2 * R_min_forward):
        power = 142  # backward
        if omega > 0:
            turn = 100
        elif omega < 0:
            turn = 200
        else:
            turn = 150
        # kitt.drive(power, turn)
    else:
        power = 158
        turn = deg_to_pwm(np.rad2deg(omega))
        # kitt.drive(power, turn)

    if dx < 0.18 and np.any(x_target == x1):
        print('x1 reached')
        # kitt.drive(145, 150)
        time.sleep(np.abs(v / 2.3))
        # kitt.stop()
        v = 0
        # x0 = get_stationary_location(10)
        dx, omega = relative_loc(x0, x_target, alpha)

        break
    dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)  # update car status
    dx, omega = relative_loc(x0, x_target, alpha)  # update end location relative to car location
    plt.plot(x0[0], x0[1], marker='.')
    print('x0', x0)


# initial values
v = 0
start_time = time.time()
dt, t = set_time(start_time, 0)
Fa = 0

# plot starting and end location
plt.plot(x0[0], x0[1], marker='o')
plt.plot(x1[0], x1[0], marker='o')
plt.plot(x2[0], x2[1], marker='o')

x_target = x2

dx, omega = relative_loc(x1, x_target, alpha)

while dx > 0.001:
    time.sleep(0.01)

    if x0[0] < 0.25 or x0[0] > 4.55 or x0[1] < 0.25 or x0[1] > 4.55:
        power = 142  # backward
        turn = 150  # straight (but slightly turning against off-set, only noticeable when driving backward)
        # kitt.drive(power, turn)
        dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)
    elif dx < np.abs(np.sin(omega) * 2 * R_min_forward):
        power = 142  # backward
        if omega > 0:
            turn = 100
        elif omega < 0:
            turn = 200
        else:
            turn = 150
        # kitt.drive(power, turn)
    else:
        power = 158
        turn = deg_to_pwm(np.rad2deg(omega))
        # kitt.drive(power, turn)

    if dx < 0.18 and np.any(x_target == x2):
        print('x1 reached')
        # kitt.drive(145, 150)
        time.sleep(np.abs(v / 2.3))
        # kitt.stop()
        v = 0
        # x0 = get_stationary_location(10)
        dx, omega = relative_loc(x0, x_target, alpha)
        print('target', x_target)
        break

    dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)  # update car status
    dx, omega = relative_loc(x0, x_target, alpha)  # update end location relative to car location
    plt.plot(x0[0], x0[1], marker='.')
    print('x0', x0)


# stop at location
# kitt.drive(145, 150)
time.sleep(np.abs(v / 2.3))
# kitt.stop()
v = 0

# del kitt        # disconnect from kitt

# plot trajectory
plt.grid(True)
plt.xlim(0, 4.80)
plt.ylim(0, 4.80)

plt.show()
