import numpy as np
import matplotlib.pyplot as plt


def circle_line_function(phase_v, new_or, r, x_start, y_start, x_dest, y_dest):
    mirror_or = 0
    x_mirror = 0
    y_mirror = 0
    # x_mirror_orig = 0
    # y_mirror_orig = 0
    # both_mirror = 0

    # # Convert new_or to a NumPy array
    # new_or_arrow = np.array(new_or)
    # plt.quiver(x_start, y_start, 20 * np.cos(np.deg2rad(new_or_arrow)), 20 * np.sin(np.deg2rad(new_or_arrow)), 'black', linewidth=2)
    # Plot an arrow indicating the orientation
    arrow_length = 34.5
    arrow_dx = arrow_length * np.cos(np.deg2rad(new_or))
    arrow_dy = arrow_length * np.sin(np.deg2rad(new_or))
    plt.arrow(x_start, y_start, arrow_dx, arrow_dy, color='black', width=0.8)


    phase_v = phase_v % 360

    if 90 < phase_v < 180: # Q2 so positive y and negative x
        print("Q2")
        x_mirror = 1 # this tells us that we need to invert x_mirroring at the end

        # shifts the x value of the destination to the right of the starting point
        # in this case y should be the same
        x_dest = x_dest + 2 * (x_start - x_dest) #mirror w.r.t the vertical
        phase_v = 180 - phase_v # mirror the phase of v properly
        new_or = 2 * (90 - new_or) + new_or
        new_or = new_or % 360

    if 270 < phase_v < 360: #so positive x and negative y
        print("Q4")
        y_mirror = 1

        # shifts the y coordinate of the destination to above the starting point
        y_dest = y_dest + 2 * (y_start - y_dest) #mirror w.r.t the horizontal
        phase_v = 360 - phase_v #mirror the phase properly
        new_or = -new_or
        new_or = new_or % 360

    if 180 < phase_v < 270: #so negative x and negative y
        print("Q3")
        y_mirror = 1
        x_mirror = 1
        x_dest = x_dest + 2 * (x_start - x_dest) #mirror w.r.t the vertical
        y_dest = y_dest + 2 * (y_start - y_dest) #mirror w.r.t the horizontal
        phase_v = phase_v - 180
        new_or = new_or + 180
        new_or = new_or % 360
    print("Q1") #else displacement vector is in Q1
    if phase_v > new_or:  #if phase displacement vector > orientation
        print("orientation mirrored")
        mirror_or = 1 #variable used to see if we need to mirror at the end
        beta = phase_v - new_or
        new_or = new_or + 2 * beta

    #calculate the center of the turn circle
    # p_lowR = new_or - 90
    # #rotate [r;0] by p_lowr and offset it by the start point to make the corresponding center point
    #
    # center_x, center_y = rotate([r, 0], p_lowR)
    # center_x += x_start
    # center_y += y_start

    # Compare with the previous method
    center_x = x_start + r * np.cos(np.deg2rad(new_or - 90))
    center_y = y_start + r * np.sin(np.deg2rad(new_or - 90))

    print("Center turn circle:", center_x, center_y)
    # print("Center using formula:", x_center_formula, y_center_formula)
    plt.plot(center_x, center_y, marker='x', color='green', markersize=10)

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
    print("used intersection (x,y)", intersect)

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
    l1_length = np.linalg.norm(l1_vector)
    print('lenght straight from vector',l1_length )



    #initially take [1l,0] then rotate and offset it
    #line_coords = np.array([l1],[0])
    #line_coords = rotate(line_coords,new_or-alpha) + intersect


    #the boundary points have to be between intersect and start point
    if new_or > phase_v:
        # upper bovel
        print('upper bovel')
        # x_short = x[np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360)]
        # y_short = y[np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360)]

        # # Convert the indices to integers using astype()
        # indices = np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360).astype(int)
        # # Use the indices for slicing
        # x_short = x[indices]
        # new_or = new_or - np.round(alpha)
        #
        # # Convert the indices to integers using astype()
        # indices = np.mod(np.arange(np.abs(90 + new_or - np.round(alpha)), np.abs(90 + new_or)), 360).astype(int)
        # # Use the indices for slicing
        # y_short = y[indices]
        x_short = x[int(np.mod(np.abs(90 + new_or - np.round(np.rad2deg(alpha))), 360)):int(np.mod(np.abs(90 + new_or), 360))]
        y_short = y[int(np.mod(np.abs(90 + new_or - np.round(np.rad2deg(alpha))), 360)):int(np.mod(np.abs(90 + new_or), 360))]
        new_or = new_or - np.round(np.rad2deg(alpha))
    else:
        # lower bovel
        print('lower bovel')
        x_short = x[int(np.mod(np.abs(180 + new_or), 360)):int(np.mod(np.abs(180 + new_or + np.round(np.rad2deg(alpha))), 360))]
        y_short = y[int(np.mod(np.abs(180 + new_or), 360)):int(np.mod(np.abs(180 + new_or + np.round(np.rad2deg(alpha)))), 360)]
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
        # beta has to be recalculated for when there is mirroring
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

    if x_mirror == 1 and y_mirror == 0:
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
    plt.plot(x_short, y_short, 'r--')
    plt.plot([x_dest, x_short[0]], [y_dest, y_short[0]], 'g--')

    x_start = x_dest
    y_start = y_dest

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

