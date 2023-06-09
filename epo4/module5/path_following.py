import time
import math
from KITT import

def pathfollowing(alpha_d, dir, l_line_cm, voltage_battery):
    c_battery = (voltage_battery / 18.8) ** 2
    v_real_circle = c_battery * 0.28
    v_real_line = c_battery * 0.41

    t_acc = 0.2
    t_brake = 0.2
    r_circle = 0.525

    v_acc = 'M165'
    v_circle = 'M154'
    v_line = 'M152'
    v_brake = 'M135'
    v_stop = 'M150'

    phi_left = 'D200'
    phi_right = 'D100'
    phi_line = 'D155'

    alpha = (alpha_d / 180) * math.pi
    l_line = l_line_cm / 100

    t_circle = (r_circle * alpha) / v_real_circle - t_acc
    t_line = l_line / v_real_line

    # drive circle
    if alpha == 0:
        EPOCommunications('transmit', phi_line)  # steer straight
    elif dir == 'l':
        EPOCommunications('transmit', phi_left)  # steer left
    else:
        EPOCommunications('transmit', phi_right)  # steer right

    EPOCommunications('transmit', v_acc)  # accelerate
    tic = time.time()
    while True:
        if time.time() - tic >= t_acc:
            break

    EPOCommunications('transmit', v_circle)  # constant speed circle
    tic = time.time()
    while True:
        if time.time() - tic >= t_circle - t_acc:
            break
        # check HERE for collision avoidance

    # drive line
    EPOCommunications('transmit', phi_line)  # steer straight
    EPOCommunications('transmit', v_line)  # constant speed line
    tic = time.time()
    while True:
        if time.time() - tic >= t_line:
            break
        # check HERE for collision avoidance

    EPOCommunications('transmit', v_brake)  # brake
    tic = time.time()
    while True:
        if time.time() - tic >= t_brake:
            break

    EPOCommunications('transmit', v_stop)  # standstill
