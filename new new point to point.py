import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from KITT import*
from epo4.Module2.Module2_mic_array.get_stationary_location import*

def deg_to_pwm(angle):
    pwm_value = round(50 * angle * 1.1 / phi_max + MIN_PWM + 50)
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
    Fa = np.cos(phi_rad*(0.3*np.pi/np.radians(phi_max))) * acceleration_force(fa_max, power)
    a = acceleration(v_old, Fa, m)
    v = v_old + a * DT

    if phi_rad != 0:  # if the car turns
        R = radius(phi_rad, v)
        delta_theta = (v_old * np.sin(phi_rad) / L)
        # delta_theta = DT*(v+v_old)/(2*R)
        # print('dt', DT)
        theta = (delta_theta * DT)
        d_new = np.array([np.cos(alpha + theta), np.sin(alpha + theta)])
        x_new = np.array([R * (-np.sin(alpha) + np.sin(alpha + theta)),
                          R * (np.cos(alpha) - np.cos(alpha + theta))]) + old_x0
    else:  # if the car drives straight
        d_new = np.array([np.cos(alpha), np.sin(alpha)])
        x_new = old_x0 + (v+v_old)/2 * DT * d_new
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
        R = L / np.tan(phi_rad)-L*np.tan(phi)
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


# class KITT:
#     def __init__(self, comport):  # called when the class is used to create a new object
#         self.serial = serial.Serial(comport, baudrate=115200, rtscts=True)
#
#     def set_speed(self, speed):
#         fspeed = f"M{speed}\n"
#         self.serial.write(fspeed.encode())
#
#     def set_angle(self, angle):
#         fangle = f"D{angle}\n"
#         self.serial.write(fangle.encode())
#
#     def stop(self):
#         power = 150
#         turn = 150
#         self.set_angle(turn)
#         self.set_speed(power)
#         return power, turn
#
#     def brake(self, speed):
#         brake_power = (np.abs(speed) / speed) * 5 + 150
#         brake_time = np.abs(speed / 2.3)
#         start = time.time()
#         T = 0
#         while T <= brake_time:
#             self.set_speed(brake_power)
#             T = T + time.time() - start
#
#     def drive(self, power, turn):
#         self.set_angle(turn)
#         self.set_speed(power)
#
#     def __del__(self):
#         self.serial.close()


# Define constants
# Fa_max = 10.615                 # Accelerating force Max.
b = 3.81        # Constant for linear drag force
c = 0.3         # Constant for quadratic drag force
Fa_max0 = b * 2.35 + c * pow(2.35, 2)       # Accelerating force Max.
voltage = 20      # battery voltage of the car
Fb_max = 17.7 * (voltage/17.7)**2                # Brake force Max.
Fa_max = Fa_max0 * (voltage/17.7)**2
m = 5.6         # Mass of car
L = 0.335       # Length of car
phi_max = 28         # Max. steering angle

# limit conditions
R_min_forward = radius(np.radians(phi_max), 1)
R_min_backward = radius(np.radians(phi_max), -1)

MIN_PWM = 100
MAX_PWM = 200

# transmitting connection takes place over port 6
comport = 'COM6'
kitt = KITT(comport)
kitt.set_beacon()       # create KITT object

# determine begin and end location
x0 = np.array([int(input('x0: ', )) / 100, int(input('y0: ', )) / 100])  # [x0,y0] starting location
alpha = np.radians(int(input('starting orientation: ', )))  # starting orientation angle with x-axis
d0 = np.array([np.cos(alpha), np.sin(alpha)])  # starting orientation vector
x1 = np.array([int(input('x1: ', )) / 100, int(input('y1: ', )) / 100])  # [x1, y1] end location
x2 = np.array([int(input('x2: ', )) / 100, int(input('y2: ', )) / 100])  # [x1, y1] end location

# x0 = np.array([3.8, 3.8])  # [x0,y0] starting location
# alpha = np.radians(180)  # starting orientation angle with x-axis
# d0 = np.array([np.cos(alpha), np.sin(alpha)])  # starting orientation vector
# x1 = np.array([2.4, 2.4])  # [x1, y1] end location
# x2 = np.array([0.4, 0.4])  # [x1, y1] end location

# print('starting in:    5')
# time.sleep(1)
# print('starting in:    4')
time.sleep(1)
print('starting in:    3')
time.sleep(1)
print('starting in:    2')
time.sleep(1)
print('starting in:    1')
time.sleep(1)

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

    # barriers
    if x0[0] < 0.18 or x0[0] > 4.62 or x0[1] < 0.18 or x0[1] > 4.62:
        kitt.brake(v)
        kitt.stop()
        dt, t, v, x0, d0, alpha = measure_loc(t, v, m, 150, L, alpha, 145, x0, Fb_max)
        power = 142  # backward
        turn = 150  # straight (but slightly turning against off-set, only noticeable when driving backward)
        while x0[0] < 0.45 or x0[0] > 4.35 or x0[1] < 0.45 or x0[1] > 4.35:
            kitt.drive(power, turn)
            dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)

    elif v <= 0 and dx < np.abs(np.sin(omega) * 2 * R_min_forward):
        power = 142  # backward
        turn = deg_to_pwm(np.rad2deg(-omega))
        kitt.drive(power, turn)
    else:
        power = 158
        turn = deg_to_pwm(np.rad2deg(omega))
        kitt.drive(power, turn)

    if dx < 0.05 and np.any(x_target == x1):
        print('x1 reached')
        kitt.brake(v)
        kitt.stop()
        power = 150
        turn = 150
        v = 0
        Location = get_stationary_location(10)
        # Location = np.array([x0[0] + 0.1, x0[1] + 0.1])
        x_model = x0
        if Location[0] > x0[0] + 0.4 or Location[1] > x0[1] + 0.4:
            x0 = Location
        else:
            x0 = np.array([(x_model[0] + Location[0]) / 2, (x_model[1] + Location[1]) / 2])
        print('x0 ', x0)
        dx, omega = relative_loc(x0, x_target, alpha)
        if dx < 0.3:
            input('press enter to start', )
            x_target = x2
        dt, t = set_time(start_time, t)
        print('target', x_target)
    elif dx < 0.1 and np.any(x_target == x2):
        print('x2 reached')
        kitt.brake(v)
        kitt.stop()     # kitt.drive(150,150)
        power = 150
        turn = 150
        v = 0
        Location = get_stationary_location(10)
        # Location = np.array([x0[0]+0.1, x0[1]+0.1])
        x_model = x0
        if Location[0] > x0[0]+0.3 or Location[1] > x0[1]+0.3:
            x0 = Location
        else:
            x0 = np.array([(x_model[0]+Location[0])/2, (x_model[1]+Location[1])/2])
        dx, omega = relative_loc(x0, x_target, alpha)
        dt, t = set_time(start_time, t)
        if dx < 0.3:
            print('WINNERS!!!')
            print('time: ', t)
            break
        print('target ', x_target)

    dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)  # update car status
    dx, omega = relative_loc(x0, x_target, alpha)  # update end location relative to car location
    plt.plot(x0[0], x0[1], marker='.')
    print('x0 ', x0)
    # print('x0', x0)

del kitt        # disconnect from kitt

# plot trajectory
plt.grid(True)
plt.xlim(0, 4.80)
plt.ylim(0, 4.80)

plt.show()