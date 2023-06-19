import math
from epo4.module5.methode2.circle_line_path_generator2 import circle_line_path_generator
from KITT import *
from epo4.Module2.Module2_mic_array.get_stationary_location import*
from epo4.Module2.Module2_mic_array.live_recording import*

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

# set angle in range -pi to pi
def call_angle(angle):
    angle = angle % (2 * np.pi)
    if angle > np.pi:
        angle = angle - 2 * np.pi
    return angle

def set_time(start, last_time):
    interval = time.time() - last_time - start
    T = time.time() - start
    return interval, T

def total_distance_driven(t, v_old, m, Turn, total_distance_driven,L, alpha, power, old_x0, fa_max):
    DT, T = set_time(start_time, t)
    PHI = phi(Turn, phi_max)
    phi_rad = np.radians(PHI)
    phi_rad = call_angle(phi_rad)
    Fa = np.cos(phi_rad * (0.25 * np.pi / np.radians(phi_max))) * acceleration_force(fa_max, power)
    a = acceleration(v_old, Fa, m)
    v = v_old + a * DT
    total_distance_driven = total_distance_driven + v * DT
    return total_distance_driven, v,T

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# x0 = np.array([int(input('x0: ', )) / 100, int(input('y0: ', )) / 100])  # [x0,y0] starting location
# init_or= int(input('starting orientation: ', ))  # starting orientation angle with x-axis
# x1 = np.array([int(input('x1: ', )) / 100, int(input('y1: ', )) / 100])  # [x1, y1] end location
# x2 = np.array([int(input('x2: ', )) / 100, int(input('y2: ', )) / 100])  # [x1, y1] end location

init_or = int(180)  # starting orientation angle with x-axis
x0 = np.array([int(100) / 100, int(100) / 100])  # [x0,y0] starting location
x1 = np.array([int(300) / 100, int(300) / 100])  # [x1, y1] end location
x2 = np.array([int(30) / 100, int(450) / 100])  # [x1, y1] end location

#max error between location car and target
dx = 0.25
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# transmitting connection takes place over port 6
comport = 'COM7'
kitt = KITT(comport)  # create KITT object
kitt.set_beacon()
def path_following(init_or,x_start,y_start,x_dest,y_dest,voltage_battery):
    c_battery = (voltage_battery/18.8)^2 # P = v^2/R -> thus if volt change by x, P changes by x^2
    v_real_circle = c_battery*28 # v = (2*pi*r_circle)/t
    v_real_line = c_battery *41 # v = s/t



    # Fa_max = 10.615                 # Accelerating force Max.
    Fb_max = 17.7  # Brake force Max.
    b = 3.81  # Constant for linear drag force
    c = 0.2  # Constant for quadratic drag force
    Fa_max0 = b * 2.3 + c * pow(2.3, 2)  # Accelerating force Max.
    voltage_battery = 19.4
    Fa_max = Fa_max0 * voltage_battery/17.8
    m = 5.6  # Mass of car (kg)
    L = 0.335  # Length of car (meter)
    phi_max = 28  # Max. steering angle

    delay = 0.4 # delay (sec) for sending and recieving data

    l_measure = 100 # if length straight > 100, start recording

    # limit conditions
    R_min_forward = radius(np.radians(phi_max), 1)
    R_min_backward = radius(np.radians(phi_max), -1)

    MIN_PWM = 100
    MAX_PWM = 200


    #drive from point to point
    new_or, alpha, l_r, Mdir, l1_lenght = circle_line_path_generator(init_or,x_start,y_start,x_dest,y_dest)



    input("Press Enter to start challenge...")
    # initial values
    v = 0
    start_time = time.time()
    dt, t = set_time(start_time, 0)
    Fa = 0
    total_distance_driven = 0

    #drive on circle
    drive_distance_on_circle = radius * alpha
    total_distance = drive_distance_on_circle + l1_lenght
    if Mdir == 'forward':
        power = 158
        if alpha != 0:
            if l_r =='r':
                turn = 100
            elif l_r == 'l':
                turn = 200
            else:
                turn = 150
            kitt.drive(power, turn)
    if Mdir == 'backwards':
        power = 142
        if alpha != 0:
            if l_r =='r':
                turn = 200 # turn left to go right
            elif l_r == 'l':
                turn = 100 # turn right to go left
            else:
                turn = 150
            kitt.drive(power, turn)

    while total_distance - total_distance_driven > 0.1:
        time.sleep(0.01)
        if total_distance_driven > drive_distance_on_circle:
            turn = 150
            kitt.drive(power, turn)

        total_distance_driven, v, t = total_distance_driven(t, v, m, turn, total_distance_driven,L, alpha, power, old_x0, fa_max)

    print('target theoretical reached')
    kitt.drive(145, 150)
    time.sleep(np.abs(v / 2.3))
    kitt.stop() # kitt.drive(150,150)

    # get current location car
    stationary_location = get_stationary_location(10)
    error = np.sqrt((stationary_location[0] - x_dest ) ** 2 + (stationary_location[1] - y_dest) ** 2)
    if error <= dx:
        x1 = stationary_location
    else:
        x1= np.array([(x_dest+ stationary_location[0]) / 2, (y_dest + stationary_location[1]) / 2])

        dt, t = set_time(start_time, t)
    if dx < error:
        print('Target Reached, Challange Completed!!!')
        print('time: ', t)
        break









    kitt.stop()
    del kitt # disconnect from kitt





    v_acc = 10
    v_line = 20
    v_brake = 0
    v_rev = -10
    v_stop = 0
    phi_line = 0
    phi_line_rev = 180

    t_acc = 2
    t_brake = 2
    t_measure = 1

    v_real_line = v_line

    # initial values
    v = 0
    start_time = time.time()
    dt, t = set_time(start_time, 0)
    Fa = 0

    def accurate_location_FD():
        # Implementation of accurate_location_FD function is missing
        pass

    def errorcorrection(v_1, v_2, xd, yd):
        # Implementation of errorcorrection function is missing
        pass

    EPOCommunications('transmit', phi_line)  # steer straight

    EPOCommunications('transmit', v_acc)  # accelerate
    toc = 0
    while True:
        if toc >= t_acc:
            break
        toc += 1

    EPOCommunications('transmit', v_line)  # drive
    tic = 0
    while True:
        if tic >= t_measure - t_acc:
            break
        # Check for collision avoidance here

    EPOCommunications('transmit', v_brake)  # brake
    tic = 0
    while True:
        if tic >= t_brake:
            break
        tic += 1
    EPOCommunications('transmit', v_stop)  # standstill

    x1, y1 = accurate_location_FD()
    v_1 = [x1, y1]

    EPOCommunications('transmit', phi_line_rev)  # steer straight for reverse

    EPOCommunications('transmit', v_brake)  # accelerate reverse
    tic = 0
    while True:
        if tic >= t_acc:
            break
        tic += 1

    EPOCommunications('transmit', v_rev)  # drive reverse
    tic = 0
    while True:
        if tic >= t_measure - t_acc:
            break
        # Check for collision avoidance here

    EPOCommunications('transmit', v_acc)  # brake reverse
    tic = 0
    while True:
        if tic >= t_brake:
            break
        tic += 1
    EPOCommunications('transmit', v_stop)  # standstill

    x2, y2 = accurate_location_FD()
    v_2 = [x2, y2]

    v_1 = [v_2[0] + (math.cos(math.radians(180)) * (v_1[0] - v_2[0])) - (math.sin(math.radians(180)) * (v_1[1] - v_2[1])),
           v_2[1] + (math.sin(math.radians(180)) * (v_1[0] - v_2[0])) + (math.cos(math.radians(180)) * (v_1[1] - v_2[1]))]

    phi_correction, l_line, orientation_final = errorcorrection(v_1, v_2, xd, yd)

    t_line = l_line / v_real_line

    EPOCommunications('transmit', phi_correction)  # steer corrected

    EPOCommunications('transmit', v_acc)  # accelerate
    toc = 0
    while True:
        if toc >= t_acc:
            break
        toc += 1

    EPOCommunications('transmit', v_line)  # drive
    tic = 0
    while True:
        if toc >= t_line - t_acc:
            break
        # Check for collision avoidance here

    EPOCommunications('transmit', v_brake)  # brake
    tic = 0
    while True:
        if tic >= t_brake:
            break
        tic += 1
    EPOCommunications('transmit', v_stop)  # standstill

    xf, yf = accurate_location_FD()

    distance_off = math.sqrt((xd - xf) ** 2 + (yd - yf) ** 2)

    if distance_off > 60:
        x1 = xf
        y1 = yf

        EPOCommunications('transmit', phi_line_rev)  # steer straight for reverse

        EPOCommunications('transmit', v_brake)  # accelerate reverse
        tic = 0
        while True:
            if tic >= t_acc:
                break
            tic += 1

        EPOCommunications('transmit', v_rev)  # drive reverse
        tic = 0
        while True:
            if tic >= (2 * t_measure) - t_acc:
                break
            # Check for collision avoidance here

        EPOCommunications('transmit', v_acc)  # brake reverse
        tic = 0
        while True:
            if tic >= t_brake:
                break
            tic += 1
        EPOCommunications('transmit', v_stop)  # standstill

        xf, yf = accurate_location_FD()

        orientation_final = math.atan(abs(yf - y1) / abs(xf - x1)) + 180  # Q1
        if xf < x1 and yf >= y1:
            orientation_final = 180 - orientation_final  # Q2
        elif xf < x1 and yf < y1:
            orientation_final = 180 + orientation_final  # Q3
        elif xf >= x1 and yf < y1:
            orientation_final = 360 - orientation_final  # Q4

        challenge_result = 'failed'
    else:
        challenge_result = 'completed'

    return challenge_result
