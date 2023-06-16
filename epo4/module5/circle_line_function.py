import numpy as np
import matplotlib.pyplot as plt


def circle_line_function(phase_v, new_or, r, x_start, y_start, x_dest, y_dest):
    mirror_or = 0
    x_mirror = 0
    y_mirror = 0
    adjust_orientation = 0
    # x_mirror_orig = 0
    # y_mirror_orig = 0
    # both_mirror = 0

    # Plot an arrow indicating the orientation
    arrow_length = 34.5
    arrow_dx = arrow_length * np.cos(np.deg2rad(new_or))
    arrow_dy = arrow_length * np.sin(np.deg2rad(new_or))
    plt.arrow(x_start, y_start, arrow_dx, arrow_dy, color='black', width=0.8)


    if new_or < phase_v or new_or > phase_v + 180:
        print('adjust_orientation')
        adjust_orientation = 1

    print(phase_v)
    phase_v = phase_v % 360 #mapping to [0,360]
    print(phase_v)



    if 90 < phase_v < 180: # Q2 so positive y and negative x
        print("Q2")
        x_mirror = 1 # this tells us that we need to invert x_mirroring at the end

        # shifts the x value of the destination to the right of the starting point
        # in this case y should be the same
        x_dest = x_dest + 2 * (x_start - x_dest) #mirror w.r.t the vertical trough start point
        phase_v = 180 - phase_v # mirror the phase of v properly
        print(phase_v)
        new_or = 2 * (90 - new_or) + new_or
        new_or = new_or % 360

    if 270 < phase_v < 360: #so positive x and negative y
        print("Q4")
        y_mirror = 1

        # shifts the y coordinate of the destination to above the starting point
        y_dest = y_dest + 2 * (y_start - y_dest) #mirror w.r.t the horizontal
        phase_v = 360 - phase_v #mirror the phase properly
        print(phase_v)
        new_or = -new_or
        new_or = new_or % 360

    if 180 < phase_v < 270: #so negative x and negative y
        print("Q3")
        y_mirror = 1
        x_mirror = 1
        x_dest = x_dest + 2 * (x_start - x_dest) #mirror w.r.t the vertical
        y_dest = y_dest + 2 * (y_start - y_dest) #mirror w.r.t the horizontal
        phase_v = phase_v - 180
        print(phase_v)
        new_or = new_or + 180
        new_or = new_or % 360
    print("Q1") #displacement vector is in Q1
    if adjust_orientation ==1:  # phase_v > new_or  if phase displacement vector > orientation
        print("orientation mirrored")
        mirror_or = 1 #variable used to see if we need to mirror at the end
        print(phase_v)
        beta = phase_v - new_or
        new_or = new_or + 2 * beta
        new_or = new_or % 360
        print(new_or)

    # #calculate the center of the turn circle
    # p_lowR = new_or - 90
    # #rotate [r;0] by p_lowr and offset it by the start point to make the corresponding center point
    #
    # center_x_formula, center_y_formula = rotate([r, 0], p_lowR)
    # center_x_formula += x_start
    # center_y_formula += y_start

    # Compare with the previous method
    center_x = x_start + r * np.cos(np.deg2rad(new_or - 90))
    center_y = y_start + r * np.sin(np.deg2rad(new_or - 90))
    # print("Center using formula:", center_x_formula, center_y_formula)

    #length between the center of the circle and the destination
    d = np.sqrt((x_dest - center_x) ** 2 + (y_dest - center_y) ** 2)
    l1 = np.sqrt(np.abs(d ** 2 - r ** 2)) # length of the straight line section of the path
    print('Length straight line', l1)

    #now make 2 circles and find their intercection
    x_intersects, y_intersects = circcirc(center_x, center_y, r, x_dest, y_dest, l1)
    print("x_intersects",x_intersects)
    print("y_intersects",y_intersects)

    #alpha is unkown so look at which intercect is closer to the start point to find alpha
    distances = [np.sqrt((x_start - x_intersects[0]) ** 2 + (y_start - y_intersects[0]) ** 2),
                 np.sqrt((x_start - x_intersects[1]) ** 2 + (y_start - y_intersects[1]) ** 2)]
    close_idx = np.argmin(distances)
    intersect = np.array([x_intersects[close_idx], y_intersects[close_idx]])


    #after finding the closer intersect we find the length of a, which gives us alpha since the formula for a and alpha is known
    a = np.sqrt((x_start - intersect[0]) ** 2 + (y_start - intersect[1]) ** 2)
    alpha = 2 * np.arcsin(a / (2 * r))
    print(f'alpha rad: {alpha}, degree: {np.rad2deg(alpha)}')

    #preallocate with 0's
    x = np.zeros(360)
    y = np.zeros(360)
    #x_2 = zeros(360)
    #y_2 = zeros(360)

    # Generate the whole circle and cut off the points later
    for theta in range(1, 361):  # in degrees
        x[theta - 1] = r * np.cos(np.deg2rad(theta)) + center_x
        y[theta - 1] = r * np.sin(np.deg2rad(theta)) + center_y
    # for theta in range(360):
    #     x[theta] = r * np.cos(np.deg2rad(theta)) + center_x
    #     y[theta] = r * np.sin(np.deg2rad(theta)) + center_y
    #     #x_2[theta] = l1*np.cos(np.deg2rad(theta) + x_dest
    #     #y_2[theta] = l1*np.cos(np.deg2rad(theta) + y_dest

    #now make the straight line part/ Calculate the vector l1
    l1_vector = np.array([x_dest, y_dest]) - intersect
    # Calculate the angle using arctan2
    angle = np.arctan2(l1_vector[1], l1_vector[0])
    # Convert the angle to degrees
    angle_degrees = np.degrees(angle)
    print("Angle in radians:", angle)
    print("Angle in degrees:", angle_degrees)

    l1_length = np.linalg.norm(l1_vector)
    print('lenght straight from vector',l1_length )



    #initially take [1l,0] then rotate and offset it
    #line_coords = np.array([l1],[0])
    #line_coords = rotate(line_coords,new_or-alpha) + intersect


    #the boundary points have to be between intersect and start point
    print(phase_v)
    print(new_or)
    print(alpha)

    # x_short = x[int(np.mod(np.abs(90 + new_or - np.round(np.rad2deg(alpha))), 360)):int(np.mod(np.abs(90 + new_or), 360))]
    # y_short = y[int(np.mod(np.abs(90 + new_or - np.round(np.rad2deg(alpha))), 360)):int(np.mod(np.abs(90 + new_or), 360))]
    if adjust_orientation == 0:#new_or > phase_v
        # upper bovel
        print('upper bovel')
        x_short = x[np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360)]
        y_short = y[np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360)]
    #
    #     # # Convert the indices to integers using astype()
    #     # indices = np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360).astype(int)
    #     # # Use the indices for slicing
    #     # x_short = x[indices]
    #     # new_or = new_or - np.round(alpha)
    #     #
    #     # # Convert the indices to integers using astype()
    #     # indices = np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360).astype(int)
    #     # # Use the indices for slicing
    #     # y_short = y[indices]
    #
        new_or = new_or - np.round(np.rad2deg(alpha))
    else:
        # lower bovel
        print('lower bovel')
        # x_short = x[int(np.mod(np.abs(180 + new_or), 360)):int(np.mod(np.abs(180 + new_or + np.round(np.rad2deg(alpha))), 360))]
        # y_short = y[int(np.mod(np.abs(180 + new_or), 360)):int(np.mod(np.abs(180 + new_or + np.round(np.rad2deg(alpha)))), 360)]
        new_or = new_or + np.round(np.rad2deg(alpha))

    # if new_or > phase_v:
    #
    #     for theta in range(int(np.round(np.rad2deg(alpha)))):
    #         x_short[theta], y_short[theta] = rotate([x[theta], y[theta]], new_or)
    #         x_short[theta] += x_start
    #         y_short[theta] += y_start
    # else:
    #     for theta in range(int(np.round(np.rad2deg(alpha)))):
    #         x_short[theta], y_short[theta] = rotate(
    #             [x[theta + 360 - int(np.round(np.rad2deg(alpha)))], y[theta + 360 - int(np.round(np.rad2deg(alpha)))]],
    #             new_or)
    #         x_short[theta] += x_start
    #         y_short[theta] += y_start

    # if x_mirror == 1 and y_mirror == 0:
    #     phase_v = 180 - phase_v
    #
    # if x_mirror == 0 and y_mirror == 1:
    #     phase_v = 360 - phase_v

    both_mirror = x_mirror * y_mirror
    # if both_mirror == 1:
    #     phase_v = 360 - phase_v
    # Now plot the path

    if mirror_or == 1:
        print('remirroring orientation')
        # beta has to be recalculated for when there is mirroring
        print(phase_v)
        print(new_or)
        beta = phase_v - new_or
        new_or = new_or + 2 * beta
        for i in range(round(np.rad2deg(alpha))):
            x_short[i] = x_short[i] - x_start
            y_short[i] = y_short[i] - y_start
            # then rotate the points by the appropriate angle (each point has a different angle)
            angle = -2 * (np.arctan2(y_short[i], x_short[i]) * 180 / np.pi - phase_v)
            x_short[i], y_short[i] = rotate(np.array([x_short[i], y_short[i]]), angle)
            x_short[i] = x_short[i] + x_start
            y_short[i] = y_short[i] + y_start

        #reflect point for plotting
        intersect_x, intersect_y = reflect_point(intersect[0],intersect[1],x_start,y_start,x_dest,y_dest)
        plt.plot(intersect_x, intersect_y, marker='o', color='black', markersize=5)
        print(f"used intersection (x,y): ({intersect_x},{intersect_y})")

        center_x, center_y = reflect_point(center_x,center_y,x_start,y_start,x_dest,y_dest)
        print("Center turn circle:", center_x, center_y)
        plt.plot(center_x, center_y, marker='x', color='green', markersize=10)
    else: #only used for plotting points
        print('plot points')
        plt.plot(intersect[0], intersect[1], marker='o', color='black', markersize=5)
        print(f"used intersection (x,y): ({intersect[0]},{intersect[1]})")

        plt.plot(center_x, center_y, marker='x', color='green', markersize=10)
        print("Center turn circle:", center_x, center_y)

    if x_mirror == 1 and y_mirror == 0:
        print('re mirroring Q2')
        x_dest = x_dest + 2 * (x_start - x_dest)
        new_or = 180 - new_or
        new_or = new_or % 360
        for i in range(round(np.rad2deg(alpha))):
            x_short[i] = x_short[i] - x_start
            y_short[i] = y_short[i] - y_start

            # then rotate the points by the appropriate angle (each point has a different angle)
            angle = 180 - 2 * (np.arctan2(y_short[i], x_short[i]) * 180 / np.pi)
            x_short[i], y_short[i] = rotate(np.array([x_short[i], y_short[i]]), angle)
            x_short[i] = x_short[i] + x_start
            y_short[i] = y_short[i] + y_start

    if y_mirror == 1 and x_mirror == 0:
        print('re mirroring Q4')
        y_dest = y_dest + 2 * (y_start - y_dest)
        new_or = -new_or
        new_or = new_or % 360
        for i in range(round(np.rad2deg(alpha))):
            x_short[i] = x_short[i] - x_start
            y_short[i] = y_short[i] - y_start

            # then rotate the points by the appropriate angle (each point has a different angle)
            angle = -2 * (np.arctan2(y_short[i], x_short[i]) * 180 / np.pi)
            x_short[i], y_short[i] = rotate(np.array([x_short[i], y_short[i]]), angle)
            x_short[i] = x_short[i] + x_start
            y_short[i] = y_short[i] + y_start

    if both_mirror == 1:
        print('re mirroring Q3')
        x_dest = x_dest + 2 * (x_start - x_dest)
        y_dest = y_dest + 2 * (y_start - y_dest)
        new_or = 180 - new_or
        new_or = new_or % 360
        for i in range(round(np.rad2deg(alpha))):
            x_short[i] = x_short[i] - x_start
            y_short[i] = y_short[i] - y_start

            # then rotate the points by the appropriate angle (each point has a different angle)
            angle = np.arctan2(y_short[i], x_short[i]) * 180 / np.pi
            x_short[i], y_short[i] = rotate(np.array([x_short[i], y_short[i]]), angle)
            x_short[i] = x_short[i] + x_start
            y_short[i] = y_short[i] + y_start


    x_short = x_short.flatten() #reshapes x_short into a column vector
    y_short = y_short.flatten() #reshapes x_short into a column vector
    plt.plot(x_short, y_short, 'r--')   #plot turn
    plt.plot([x_dest, x_short[0]], [y_dest, y_short[0]], 'g--') #plot straigtline

    x_start = x_dest
    y_start = y_dest

    print(new_or)
    if mirror_or == 1:
        l_r = 'l'
    else:
        l_r = 'r'
    print('turn',l_r)
    return new_or, x_start,y_start,alpha,x_short,y_short,l_r,x_mirror,y_mirror,both_mirror, l1_vector



def rotate(point, angle):
    angle_rad = np.deg2rad(angle)
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                [np.sin(angle_rad), np.cos(angle_rad)]])
    return np.dot(rotation_matrix, point)


def circcirc(x1, y1, r1, x2, y2, r2):
    d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = np.sqrt(r1 ** 2 - a ** 2)

    x_mid = x1 + a * (x2 - x1) / d
    y_mid = y1 + a * (y2 - y1) / d

    x3 = x_mid + h * (y2 - y1) / d
    y3 = y_mid - h * (x2 - x1) / d

    x4 = x_mid - h * (y2 - y1) / d
    y4 = y_mid + h * (x2 - x1) / d

    return [x3, x4], [y3, y4]

def reflect_point(a, b, x0, y0, x1, y1):
    # Calculate the slope of the line
    m = (y1 - y0) / (x1 - x0)

    # y intercept
    c = (x1*y0-x0*y1)/(x1-x0)

    # d
    d = (a + (b-c)*m)/(1+m**2)

    reflected_a = 2*d - a
    reflected_b = 2*d*m - b +2*c
    return reflected_a, reflected_b

