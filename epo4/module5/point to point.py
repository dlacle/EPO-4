import serial
import time
import re
import numpy as np
import matplotlib.pyplot as plt

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
    else:
        phi = 0
    return phi

# determining location x1 with respect to x0
def beta(x0, y0, x1, y1):
    dx = np.array([x1-x0, y1-y0])                 # distance/direction vector between location 0 and 1
    angle_beta = np.arctan(dx[1]/dx[0])               # angle of dx vector with positive x-axis (requested direction)
    return angle_beta

class KITT:
    def __init__(self, comport):        # called when the class is used to create a new object
        self.serial = serial.Serial(comport, baudrate=115200, rtscts=True)

    def set_speed(self, speed):
        fspeed = f"M{speed}\n"
        self.serial.write(fspeed.encode())

    def brake(self, speed):
        power = -(speed/(np.abs(speed)))*5+150
        self.set_speed(power)
    def set_angle(self, angle):
        fangle = f"D{angle}\n"
        self.serial.write(fangle.encode())

    def stop(self):
        self.set_angle(150)
        self.set_speed(150)

    def __del__(self):
        self.serial.close()

    def turn(self, direction):
        if direction == 'hard left':
            self.set_angle(200)
        elif direction == 'hard right':
            self.set_angle(100)
        elif direction == 'right':
            self.set_angle(125)
        elif direction == 'left':
            self.set_angle(125)

# Define constants
Fa_max = 11     # Accelerating force Max.
Fb_max = 14     # Brake force Max.
b = 3.81   # Constant for linear drag force
c = 0.35  # Constant for quadratic drag force
m = 5.6     # Mass of car
L = 0.335   # Length of car

# transmitting connection takes place over port 6
comport = 'COM8'
kitt = KITT(comport)


# determine begin and end location
x0 = np.array([int(input('x0: ', ))/100, int(input('y0: ', ))/100])      # [x0,y0]
x_new = x0
alfa = np.radians(int(input('starting orientaion: ', )))        # starting orientation angle with x-axis
d0 = np.array([np.cos(alfa), np.sin(alfa)])                     # starting orientation vector
d_new = d0
x1 = np.array([int(input('x1: ', ))/100, int(input('y1: ', ))/100])      # [x1, y1]

dx_vector = np.array([x1[0] - x0[0], x1[1] - x0[1]])  # distance/direction vector between location 0 and 1
dx = np.sqrt(pow(dx_vector[0],2)+pow(dx_vector[1],2))   # distance to location 1
angle_beta = beta(x0[0], x0[1], x1[0], x1[1])

Theta = 0

while dx >= 0.01:
    dt = 0
    v = 0
    # if next location is not reachable in 1 manoeuvre, turn while getting distance.
    while np.pi/3 <= angle_beta <= 2*np.pi/3 and dx <=1.45:
        start_time = time.time()
        t = time.time()-start_time
        kitt.turn('hard right')
        phi_rad = np.radians(-25)
        power = 142
        Fa = np.cos(phi_rad) * acceleration_force(Fa_max, power)
        R = radius(phi_rad, power)
        x_new = x0
        d_new = d0
        while Theta < np.pi/2:                              # turn backwards, right, until turned 90 degrees
            kitt.set_speed(power)

            a = acceleration(v, Fa, m)
            v = v + a * dt

            dt = time.time() - t -start_time
            t = time.time() - start_time

            delta_Theta = v * np.sin(phi_rad) / L
            Theta = (Theta + delta_Theta * dt)

            d_new = np.array([np.cos(alfa + Theta), np.sin(alfa + Theta)])
            x_new = np.array([R * (-np.sin(alfa) + np.sin(alfa + Theta)),
                         R * (np.cos(alfa) - np.cos(alfa + Theta))]) + x0

            dx_vector = np.array([x1[0] - x_new[0], x1[1] - x_new[1]])  # distance/direction vector between location 0 and 1
            dx = np.sqrt(pow(dx_vector[0], 2) + pow(dx_vector[1], 2))  # distance to location 1

        kitt.stop()
        x0 = x_new
        d0 = d_new
        alfa = alfa + Theta
        Theta = 0
        print('1e if loop')

        angle_beta = beta(x0[0], x0[1], x1[0], x1[1])
        dx_vector = np.array([x1[0] - x0[0], x1[1] - x0[1]])  # distance/direction vector between location 0 and 1
        dx = np.sqrt(pow(dx_vector[0], 2) + pow(dx_vector[1], 2))  # distance to location 1

    if angle_beta >= -2*np.pi/3 and angle_beta <= -np.pi/3 and dx <=1.45 :
        start_time = time.time()
        t = time.time()-start_time
        kitt.turn('hard left')
        phi_rad = np.radians(25)
        power = 142
        Fa = np.cos(phi_rad) * acceleration_force(Fa_max, power)
        R = radius(phi_rad, power)

        while Theta > -np.pi/2:                     # turn backwards, left, until turned -90 degrees
            kitt.set_speed(power)

            a = acceleration(v, Fa, m)
            v = v + a * dt

            dt = time.time() - t - start_time
            t = time.time() - start_time

            delta_Theta = v * np.sin(phi_rad) / L
            Theta = (Theta + delta_Theta * dt)

            d0 = np.array([np.cos(alfa + Theta), np.sin(alfa + Theta)])
            x0 = np.array([R * (-np.sin(alfa) + np.sin(alfa + Theta)),
                         R * (np.cos(alfa) - np.cos(alfa + Theta))]) + x0

            dx_vector = np.array([x1[0] - x_new[0], x1[1] - x_new[1]])  # distance/direction vector between location 0 and 1
            dx = np.sqrt(pow(dx_vector[0], 2) + pow(dx_vector[1], 2))  # distance to location 1

        kitt.stop()
        alfa = alfa + Theta
        Theta = 0
        print('2e if loop')

        angle_beta = beta(x0[0], x0[1], x1[0], x1[1])
        dx_vector = np.array([x1[0] - x0[0], x1[1] - x0[1]])  # distance/direction vector between location 0 and 1
        dx = np.sqrt(pow(dx_vector[0], 2) + pow(dx_vector[1], 2))  # distance to location 1

    # drive forwards while turning hard to align to the destination

    start_time = time.time()
    t = time.time() - start_time

    while dx >= 0.01:
        print('while loop')

        if angle_beta < alfa:                           # drive forward while turning right when the end location is located right of current location
            kitt.turn('hard right')
            phi_rad = np.radians(-25)
            power = 158
            Fa = np.cos(phi_rad) * acceleration_force(Fa_max, power)
            R = radius(phi_rad, power)
            kitt.set_speed(power)

            a = acceleration(v, Fa, m)
            v = v + a * dt

            dt = time.time() - t - start_time
            t = time.time() - start_time

            delta_Theta = v * np.sin(phi_rad) / L
            Theta = (Theta + delta_Theta * dt)

            d0 = [np.cos(alfa + Theta), np.sin(alfa + Theta)]
            x0 = [R * (-np.sin(alfa) + np.sin(alfa + Theta)),
                  R * (np.cos(alfa) - np.cos(alfa + Theta))] + x0
            print('while: rechts')

        elif angle_beta > alfa:                                     # drive forward while turning left when end location is located left of current location
            kitt.turn('hard left')
            phi_rad = np.radians(25)
            power = 158
            Fa = np.cos(phi_rad) * acceleration_force(Fa_max, power)
            R = radius(phi_rad, power)
            kitt.set_speed(power)

            a = acceleration(v, Fa, m)
            v = v + a * dt

            dt = time.time() - t - start_time
            t = time.time() - start_time

            delta_Theta = v * np.sin(phi_rad) / L
            Theta = (Theta + delta_Theta * dt)

            d0 = [np.cos(alfa + Theta), np.sin(alfa + Theta)]
            x0 = [R * (-np.sin(alfa) + np.sin(alfa + Theta)),
                  R * (np.cos(alfa) - np.cos(alfa + Theta))] + x0

            print('while: links')
        else:                                                       # drive straight when the end location is located infront of current location
            kitt.set_angle(150)
            phi_rad = np.radians(0)
            power = 158
            Fa = np.cos(phi_rad) * acceleration_force(Fa_max, power)
            R = radius(phi_rad, power)
            kitt.set_speed(power)

            a = acceleration(v, Fa, m)
            v = v + a * dt

            dt = time.time() - t - start_time
            t = time.time() - start_time

            delta_Theta = v * np.sin(phi_rad) / L
            Theta = (Theta + delta_Theta * dt)

            d0 = [np.cos(alfa + Theta), np.sin(alfa + Theta)]
            x0 = [R * (-np.sin(alfa) + np.sin(alfa + Theta)),
                  R * (np.cos(alfa) - np.cos(alfa + Theta))] + x0
            print('while: rechtdoor')

        angle_beta = beta(x0[0],x0[1],x1[0],x1[1])
        dx_vector = np.array([x1[0] - x0[0], x1[1] - x0[1]])  # distance/direction vector between location 0 and 1
        dx = np.sqrt(pow(dx_vector[0], 2) + pow(dx_vector[1], 2))  # distance to location 1
        alfa = alfa + Theta
        Theta = 0
        print(x0)

    kitt.stop()



del kitt        # disconnect from kitt