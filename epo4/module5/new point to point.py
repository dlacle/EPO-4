import serial
import time
import numpy as np
import matplotlib.pyplot as plt


# dt, t = set_time(start_time, t)
def set_time(start, last_time):
    interval = time.time() - last_time - start
    T = time.time() - start
    return interval, T


# relative location of end location x1
def relative_loc(x0, x1, alpha):
    dx_vector = np.array([x1[0] - x0[0], x1[1] - x0[1]])  # distance/direction vector between location 0 and 1
    dx = np.sqrt(pow(dx_vector[0], 2) + pow(dx_vector[1], 2))  # distance to location 1
    angle_beta = beta(x0[0], x0[1], x1[0], x1[1])  # angle between dx_vector and positive x-axis
    omega = angle_beta - alpha  # angle between dx_vector and d0
    omega = call_angle(omega)
    return dx, omega


# measure location according to the car model
# dt, t, v, x0, d0, alpha, plot = measure_loc(dt, t, v, Fa, m, turn, L, alpha, power, x0)
def measure_loc(dt, t, v_old, m, Turn, L, alpha, power, old_x0):
    DT, T = set_time(start_time, t)
    PHI = phi(Turn, phi_max)
    phi_rad = np.radians(PHI)
    phi_rad = call_angle(phi_rad)
    Fa = np.cos(phi_rad) * acceleration_force(Fa_max, power)
    a = acceleration(v_old, Fa, m)
    v = v_old + a * dt

    if phi_rad != 0:            # if the car turns
        R = radius(phi_rad, power)
        delta_theta = (v * np.sin(phi_rad) / L) * dt
        theta = (delta_theta * dt)
        d_new = np.array([np.cos(alpha + theta), np.sin(alpha + theta)])
        x_new = np.array([R * (-np.sin(alpha) + np.sin(alpha + theta)),
                          R * (np.cos(alpha) - np.cos(alpha + theta))]) + old_x0
    else:                       # if the car drives straight
        d_new = d0
        x_new = old_x0 + v * dt * d0
        theta = 0

    X0 = x_new
    D0 = d_new
    Alpha = alpha + theta
    Alpha = call_angle(Alpha)
    plot = plt.plot(x_new[0], x_new[1], marker='.')
    return DT, T, v, X0, D0, Alpha, plot


# Define radius
def radius(phi_rad, power):
    # estimation of R
    if phi_rad != 0 and power >= 150:
        R = L / np.tan(phi_rad)
    elif phi_rad != 0 and power <= 150:
        R = L / np.tan(phi_rad) - L * np.tan(phi_rad)
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
        Fa = Fa_max * (3.7687 + (power - 157) * 1.256)
    elif power >= 140 and power < 145:
        Fa = Fa_max * (-6.667 + (power - 140) * 1.333)
    elif power >= 135 and power < 140:
        Fa = -Fa_max / (power - 135)
    else:
        Fa = 0
    return Fa


# Define function for the acceleration with respect to time
def acceleration(v, Fa, m):
    F_drag = b * np.abs(v) + c * v ** 2  # Drag force based on velocity using given expression
    a = 0
    if Fa >= 0 and v >= 0:
        a = (Fa - F_drag) / m  # Acceleration based on forces
    elif Fa < 0 and v <= 0:
        a = (Fa + F_drag) / m
    elif Fa < 0 and v >= 0:
        a = (Fa - F_drag) / m
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
    angle_beta = np.arctan(dx[1] / dx[0])  # angle of dx vector with positive x-axis (requested direction)
    angle_beta = call_angle(angle_beta)
    return angle_beta


# set angle in range -pi to pi
def call_angle(angle):
    angle = angle % (2*np.pi)
    if angle > np.pi:
        angle = angle - 2*np.pi
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
        start_time = time.time()
        t = 0
        while t <= brake_time:
            self.set_speed(brake_power)
            t = t + time.time() - start_time

    def drive(self, power, turn):
        self.set_angle(turn)
        self.set_speed(power)

    def __del__(self):
        self.serial.close()


# Define constants
# Fa_max = 10.615                 # Accelerating force Max.
Fb_max = 14.318  # Brake force Max.
b = 2.7  # Constant for linear drag force
c = 0.27  # Constant for quadratic drag force
Fa_max = b * 2.2 + c * pow(2.2, 2)  # Accelerating force Max.
m = 5.6  # Mass of car
L = 0.335  # Length of car
phi_max = 24.5  # Max. steering angle

# limit conditions
R_min_forward = radius(np.radians(phi_max), 165)
R_min_backward = radius(np.radians(phi_max), 135)

# transmitting connection takes place over port 6
# comport = 'COM8'
# kitt = KITT(comport)                                                    # create KITT object

# determine begin and end location
x0 = np.array([int(input('x0: ', )) / 100, int(input('y0: ', )) / 100])  # [x0,y0] starting location
alpha = np.radians(int(input('starting orientaion: ', )))  # starting orientation angle with x-axis
d0 = np.array([np.cos(alpha), np.sin(alpha)])  # starting orientation vector
x1 = np.array([int(input('x1: ', )) / 100, int(input('y1: ', )) / 100])  # [x1, y1] end location

# relative location of  car and end-location x1
dx, omega = relative_loc(x0, x1, alpha)

# initial values
v = 0
start_time = time.time()
dt, t = set_time(start_time, 0)
Fa = 0

# plot starting and end location
plt.plot(x0[0], x0[1], marker='o')
plt.plot(x1[0], x1[0], marker='o')

# drive from point to point
while dx >= 0.18:
    time.sleep(0.07)
    dx, omega = relative_loc(x0, x1, alpha)     # update end location relative to car location

    # check for barriers
    if x0[0] <= 0.25 and (alpha >= 0.5 * np.pi or alpha <= -0.5 * np.pi):       # barrier left
        # kitt.brake(v)
        power = 142
        turn = 150
        # kitt.drive(power, turn)       # drive backward for 'sleep' seconds
        sleep = 0.3
        time.sleep(0.3)
        # kitt.stop()
        dt, t, v, x0, d0, alpha, plot = measure_loc(dt + sleep, t, v, m, turn, L, alpha, power, x0)
        dx, omega = relative_loc(x0, x1, alpha)
        if -0.5 * np.pi > alpha >= -np.pi:
            turn = 100
        else:
            turn = 200
        while (alpha >= 0.5 * np.pi or alpha <= -0.5 * np.pi) and 0.25 <= x0[1] <=4.55:
            # kitt.drive(power, turn)
            dt, t, v, x0, d0, alpha, plot = measure_loc(dt, t, v, m, turn, L, alpha, power, x0)
            dx, omega = relative_loc(x0, x1, alpha)
            print('barrier left')
            print('alpha: ', alpha)
    # elif x0[0] >= 4.55 and (alpha <= 0.5 * np.pi or alpha >= -0.5 * np.pi):      # barrier right
    #     # kitt.brake(v)
    #     power = 142
    #     turn = 150
    #     # kitt.drive(power, turn)       # drive backward for 'sleep' seconds
    #     sleep = 0.3
    #     time.sleep(0.3)
    #     # kitt.stop()
    #     dt, t, v, x0, d0, alpha, plot = measure_loc(dt + sleep, t, v, m, turn, L, alpha, power, x0)
    #     dx, omega = relative_loc(x0, x1, alpha)
    #     if 0.5 * np.pi > alpha >= 0:
    #         turn = 100
    #     else:
    #         turn = 200
    #     while (alpha <= 0.5 * np.pi or alpha >= -0.5 * np.pi) and 0.25 <= x0[1] <=4.55:
    #         # kitt.drive(power, turn)
    #         dt, t, v, x0, d0, alpha, plot = measure_loc(dt, t, v, m, turn, L, alpha, power, x0)
    #         dx, omega = relative_loc(x0, x1, alpha)
    #         print(x0)
    #         print(alpha)
    #         print('barrier right')
    # elif x0[1] <= 0.25 and 0 >= alpha >= -np.pi:     # barrier below
    #     # kitt.brake(v)
    #     power = 142
    #     turn = 150
    #     # kitt.drive(power, turn)       # drive backward for 'sleep' seconds
    #     sleep = 0.3
    #     time.sleep(0.3)
    #     # kitt.stop()
    #     dt, t, v, x0, d0, alpha, plot = measure_loc(dt + sleep, t, v, m, turn, L, alpha, power, x0)
    #     dx, omega = relative_loc(x0, x1, alpha)
    #     if -0.5 * np.pi < alpha <= 0:
    #         turn = 100
    #     else:
    #         turn = 200
    #     while 0 >= alpha >= -np.pi and 0.25 <= x0[0] <= 4.55:
    #         # kitt.drive(power, turn)
    #         dt, t, v, x0, d0, alpha, plot = measure_loc(dt, t, v, m, turn, L, alpha, power, x0)
    #         dx, omega = relative_loc(x0, x1, alpha)
    #         print('barrier below')
    # elif x0[1] >= 4.55 and (np.pi >= alpha >= 0):     # barrier above
    #     # kitt.brake(v)
    #     power = 142
    #     turn = 150
    #     # kitt.drive(power, turn)       # drive backward for 'sleep' seconds
    #     sleep = 0.3
    #     time.sleep(0.3)
    #     # kitt.stop()
    #     dt, t, v, x0, d0, alpha, plot = measure_loc(dt+sleep, t, v, m, turn, L, alpha, power, x0)
    #     dx, omega = relative_loc(x0, x1, alpha)
    #     if 0.5 * np.pi < alpha <= np.pi:
    #         turn = 100
    #     else:
    #         turn = 200
    #     while np.pi >= alpha >= 0 and 0.25<= x0[0] <=4.55:
    #         # kitt.drive(power, turn)
    #         dt, t, v, x0, d0, alpha, plot = measure_loc(dt, t, v, m, turn, L, alpha, power, x0)
    #         dx, omega = relative_loc(x0, x1, alpha)
    #         print(x0)
    #         print('barrier above')

    # check for obstacles
    #######
    # obstacle check code
    #######

    # get minimal distance to get to end location with only one setting (10cm buffer in radius)
    # if dx * np.abs(np.sin(omega)) < 2 * (R_min_forward + 0.05) * np.abs(np.sin(omega)):
    #     if omega >= 0:  # end location lies left of current orientation
    #         power = 142  # forward
    #         turn = 100  # right
    #     else:  # end location lies right of current orientation
    #         power = 142  # forward
    #         turn = 200  # left
    #     # kitt.drive(power, turn)
    #     print('get minimal distance')

    # end-location lies in-front or next to the car
    else:
        # if omega >= (np.pi - 0.01388 * np.pi) or omega <= (-np.pi + 0.01388 * np.pi):   # end location, directly behind car
        #     power = 142     # forward
        #     turn = 149      # straight (but slightly turning against off-set, only noticeable when driving backward)
        #     # kitt.drive(power, turn)
        #     turn = 150      # needed for measurements/calculations
        if -0.01 * np.pi <= omega <= 0.01 * np.pi:  # end location, directly in-front of car
            power = 158  # forward
            turn = 150  # straight
            # kitt.drive(power, turn)
        elif omega > 0.01 * np.pi:  # end location, left of car
            power = 158  # forward
            turn = 200  # left
            # kitt.drive(power, turn)
        elif omega < -0.01 * np.pi:  # end location, right of car
            power = 158  # forward
            turn = 100  # right
            # kitt.drive(power, turn)
    # else:   # do nothing
    # power, turn = kitt.stop()
    print('drive to destination')
    print('x0: ', x0)
    print('d0: ', d0)
    print('omega', omega)
    print('turn ', turn)
    print('power ', power)
    dt, t, v, x0, d0, alpha, plot = measure_loc(dt, t, v, m, turn, L, alpha, power, x0)     # update car status

# stop at location
# kitt.brake(v)
# kitt.stop()

# del kitt        # disconnect from kitt

# plot trajectory
plt.grid(True)
plt.xlim(0, 4.80)
plt.ylim(0, 4.80)

plt.show()
