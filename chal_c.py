from epo4.module5.methode2.ObstacleDetect import ObstacleDetect

Fb_max = 17.7  # Brake force Max.
b = 2.74  # Constant for linear drag force
c = 0.27  # Constant for quadratic drag force
Fa_max0 = b * 2.35 + c * pow(2.35, 2)  # Accelerating force Max.
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
x0 = np.array([int(200) / 100, int(100) / 100])  # [x0,y0] starting location
alpha = np.radians(int(90))  # starting orientation angle with x-axis
d0 = np.array([np.cos(alpha), np.sin(alpha)])  # starting orientation vector
x1 = np.array([int(350-200) / 100, int(350) / 100])  # [x1, y1] end location
# x2 = np.array([int(input('x2: ', )) / 100, int(input('y2: ', )) / 100])  # [x1, y1] end location

print('starting in:    5')
time.sleep(1)
print('starting in:    4')
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
# plt.plot(x2[0], x2[1], marker='o')
dis=80
x_target = x1
obs=0
dirr=0
x4=x0
dx, omega = relative_loc(x0, x_target, alpha)  # update end location relative to car location
qs = time.time()
# drive from point to point
# flag_obstacle = False
while dx > 0.001:
    time.sleep(0.01)
    dis=dis-0.3
    # barriers
    print(dis)
    print("omega",np.rad2deg(omega))

    # if ObstacleDetect(x0,x1) ==  True:
    #     obs = 1
    #
    #     # x4=x0
    #     plt.plot(x0[0], x0[1], marker='x')
    #     plt.plot(x0[0] + np.cos(dirr+np.pi)*0.60, x0[1] + np.sin(dirr+np.pi)*0.6, marker='x')
    #     plt.plot(x0[0] + np.cos(dirr+np.pi) * 0.60+0.20, x0[1] + np.sin(dirr+np.pi) * 0.6, marker='x')
    #
    #     print("z",x0[0], x0[1])
    #     # break

    if ObstacleDetect(x0,x1) ==  True : #and not flag_obstacle
        # flag_obstacle = True
        dirr = np.arctan(d0[1] / d0[0])
        dirr1 = np.arctan(d0[1] / d0[0]) + np.pi
        print(dirr1)
        if dirr>0:
            dis=300000000
            turn=deg_to_pwm(-30)
            power=158
            print("current d",np.arctan(d0[1]/d0[0]))
            print("desti",dirr-np.pi/8)



        elif dirr<0:
            turn=deg_to_pwm(30)
            power=158
            print("current d",np.rad2deg(np.arctan(d0[1]/d0[0])+np.pi))
            print("desti",)
            print(np.rad2deg(1.5/2))
            plt.plot(x0[0],x0[1], marker='x')



    elif x0[0] < 0.25 or x0[0] > 4.55 or x0[1] < 0.25 or x0[1] > 4.55:
        # kitt.brake(v)
        time.sleep(abs(v) / 2.3)
        # kitt.stop()
        dt, t, v, x0, d0, alpha = measure_loc(t, v, m, 150, L, alpha, 145, x0, Fb_max)
        power = 142  # backward
        turn = 150  # straight (but slightly turning against off-set, only noticeable when driving backward)
        # turn = deg_to_pwm(-omega)
        while x0[0] < 0.45 or x0[0] > 4.35 or x0[1] < 0.45 or x0[1] > 4.35:
            # kitt.drive(power, turn)
            dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)

    elif dx < np.abs(np.sin(omega) * 2 * R_min_forward):
        power = 142  # backward
        turn = deg_to_pwm(np.rad2deg(omega-np.pi))
        # if omega > 0:
        #     turn = 100
        # elif omega < 0:
        #     turn = 200
        # else:
        #     turn = 150
        # kitt.drive(power, turn)
    else:
        power = 158
        turn = deg_to_pwm(np.rad2deg(omega))
        # kitt.drive(power, turn)

    if dx < 0.4 and np.any(x_target == x1):
        print('x1 reached')
        # kitt.drive(145, 150)
        time.sleep(np.abs(v / 2.3))
        # kitt.stop()
        v = 0
        # Location = get_stationary_location(10)
        Location = np.array([x0[0] + 0.1, x0[1] + 0.1])
        x_model = x0
        # if Location[0] > x0[0] + 0.3 or Location[1] > x0[1] + 0.3:
        #     x0 = Location
        # else:
        #     x0 = np.array([(x_model[0] + Location[0]) / 2, (x_model[1] + Location[1]) / 2])
        # print('x0 ', x0)
        dx, omega = relative_loc(x0, x_target, alpha)
        break





    dt, t, v, x0, d0, alpha = measure_loc(t, v, m, turn, L, alpha, power, x0, Fa_max)  # update car status
    dx, omega = relative_loc(x0, x_target, alpha)  # update end location relative to car location
    plt.plot(x0[0], x0[1], marker='.')
    print('x0 ', x0)


# stop at location
# kitt.drive(145, 150)
# time.sleep(np.abs(v / 2.3))
# kitt.stop()
v = 0

# del kitt        # disconnect from kitt

# plot trajectory
plt.grid(True)
plt.xlim(0, 4.80)
plt.ylim(0, 4.80)

plt.show()
