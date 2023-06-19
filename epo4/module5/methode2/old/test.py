import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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

def reflect_point_wrt_vertical(a, b, x0):
    # Calculate the x-coordinate of the reflected point
    reflected_a = 2 * x0 - a

    # No change in the y-coordinate
    reflected_b = b

    return reflected_a, reflected_b


def path_finder(theta_degree, x0, y0, x1, y1, r):
    # Calculate the center of the first circle
    x_center = x0 + r * math.cos(math.radians(theta_degree - 90))
    print('x_center:', x_center)
    y_center = y0 + r * math.sin(math.radians(theta_degree - 90))
    print('y_center:', y_center)

    # Calculate the length of the line
    center_to_destination = math.sqrt((x_center - x1) ** 2 + (y_center - y1) ** 2)
    l_straight_line = math.sqrt(center_to_destination ** 2 - r ** 2)
    print('Length straight line',l_straight_line)
    # Find the intersection points
    alpha = math.acos(
        (r ** 2 + center_to_destination ** 2 - l_straight_line ** 2) / (2 * r * center_to_destination))
    beta = math.atan2(y1 - y_center, x1 - x_center)
    theta1 = beta + alpha
    theta2 = beta - alpha

    # Calculate the intersection points
    intersect1_x = x_center + r * math.cos(theta1)
    intersect1_y = y_center + r * math.sin(theta1)
    intersect2_x = x_center + r * math.cos(theta2)
    intersect2_y = y_center + r * math.sin(theta2)

    # Print the intersection points
    print("Intersection Point 1: ({:.2f}, {:.2f})".format(intersect1_x, intersect1_y))
    print("Intersection Point 2: ({:.2f}, {:.2f})".format(intersect2_x, intersect2_y))

    begin_to_intercept = math.sqrt((x0 - intersect1_x) ** 2 + (y0 - intersect1_y) ** 2)
    turning_angle = 2 * math.asin(begin_to_intercept / (2 * r))
    print(f'turning_angle rad:{turning_angle}, deg: {math.degrees(turning_angle)}')

    angle_l_straight_line = 0
    if l_straight_line != 0:
        # Calculate the angle of the car at the final position
        angle_l_straight_line = math.atan((y1 - intersect1_y) / (x1 - intersect1_x))
        print('angle straight line rad:',angle_l_straight_line)
    return (x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line, turning_angle,
            angle_l_straight_line)
def reflect_wrt_displacement(x0, y0, x1, y1, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y,angle_l_straight_line):
    # Reflect the center and intersection points with respect to the displacement vector
    reflected_x_center,reflected_y_center = reflect_point(x_center,y_center,x0,y0,x1,y1)
    reflected_intersect1_x, reflected_intersect1_y = reflect_point(intersect1_x, intersect1_y, x0, y0, x1, y1)
    reflected_intersect2_x, reflected_intersect2_y = reflect_point(intersect2_x, intersect2_y, x0, y0, x1, y1)

    # Calculate the reflected turning angle
    turning_angle = 2 * math.asin(math.sqrt((x0 - intersect1_x) ** 2 + (y0 - intersect1_y) ** 2) / (2 * r))
    reflected_turning_angle = math.pi - turning_angle
    print(f'turning_angle rad:{turning_angle}, reflected: {reflected_turning_angle}, reflected degree:{math.degrees(reflected_turning_angle)}')
    # Calculate the reflected angle of the car at the final position
    reflected_angle_l_straight_line = -angle_l_straight_line
    print('reflected angle straight line rad:',reflected_angle_l_straight_line)
    # Return the reflected results
    return (
        reflected_x_center, reflected_y_center, reflected_intersect1_x, reflected_intersect1_y,
        reflected_intersect2_x, reflected_intersect2_y, l_straight_line, reflected_turning_angle,
        reflected_angle_l_straight_line
    )
def reflect_wrt_vertical(x0, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y,angle_l_straight_line):
    # Reflect the center and intersection points with respect to the vertical line through (x0,y0)
    x_center_reflected_wrt_vertical, y_center_reflected_wrt_vertical = reflect_point_wrt_vertical(x_center, y_center, x0)
    intersect1_x_reflected_wrt_vertical, intersect1_y_reflected_wrt_vertical = reflect_point_wrt_vertical(intersect1_x, intersect1_y, x0)
    intersect2_x_reflected_wrt_vertical, intersect2_y_reflected_wrt_vertical = reflect_point_wrt_vertical(intersect2_x, intersect2_y, x0)

    # Calculate the reflected angle of the car at the final position
    reflected_angle_l_straight_line = -angle_l_straight_line
    print('reflected angle straight line rad:', reflected_angle_l_straight_line)
    # Return the reflected results
    return (
        x_center_reflected_wrt_vertical, y_center_reflected_wrt_vertical, intersect1_x_reflected_wrt_vertical, intersect1_y_reflected_wrt_vertical,
        intersect2_x_reflected_wrt_vertical, intersect2_y_reflected_wrt_vertical,reflected_angle_l_straight_line
    )
def plot_path(theta, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line,
              turning_angle,
              angle_l_straight_line,title):
    # Plot the straight line and the circular path
    fig, ax = plt.subplots()

    # create straight line
    ax.plot([intersect1_x, x1], [intersect1_y, y1], 'b--', label='Trajectory')
    # Create the Arc patch
    # Calculate the start and end angles for the arc
    start_angle = math.degrees(math.atan2(intersect1_y - y_center, intersect1_x - x_center))
    end_angle = start_angle + math.degrees(turning_angle)  # Calculate the end angle based on the turning angle
    print(start_angle)
    # Calculate the angle of the arc
    arc_angle = end_angle - start_angle

    center = (x_center, y_center)
    width = 2 * r
    height = 2 * r

    angle = 0
    arc = patches.Arc(center, width, height, angle=angle, theta1=start_angle, theta2=end_angle, linewidth=1,
                      edgecolor='r', linestyle='--')
    ax.add_patch(arc)
    # # Calculate the start and end angles for the arc
    # start_angle = math.degrees(math.atan2(intersect1_y - y_center, intersect1_x - x_center))
    # # print(start_angle)
    # end_angle = math.degrees(math.atan2(y0 - y_center, x0 - x_center))
    # # print(end_angle)
    # # Calculate the angle of the arc
    # arc_angle = end_angle - start_angle

    # Print the angle of the arc
    print("Angle of the arc: {:.2f} degrees".format(arc_angle))

    center = (x_center, y_center)
    width = 2 * r
    height = 2 * r
    # angle = 0# math.degrees(angle_l_straight_line) #theta_degree + math.degrees(angle_displacement)#
    angle = 0  # theta_degree + math.degrees(angle_displacement)
    arc = patches.Arc(center, width, height, angle=angle, theta1=start_angle, theta2=end_angle, linewidth=1,
                      edgecolor='r',
                      linestyle='--')
    ax.add_patch(arc)

    ax.plot(x0, y0, 'kx', label='Starting Point')
    ax.plot(x1, y1, 'kx', label='End Point')
    ax.plot(x_center, y_center, 'gx', label='Center')

    # Plot an arrow indicating the orientation
    arrow_length = 0.5
    arrow_dx = arrow_length * math.cos(theta)
    arrow_dy = arrow_length * math.sin(theta)
    ax.arrow(x0, y0, arrow_dx, arrow_dy, color='black', width=0.01)

    # Plot the displacement vector
    ax.plot([x0, x1], [y0, y1], color='blue', linestyle='-', linewidth=1)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)  # Set the title
    ax.legend()
    plt.show()
    return
def plot_path_re_mirrored(theta, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line,
              turning_angle,
              angle_l_straight_line,title):
    # Plot the straight line and the circular path
    fig, ax = plt.subplots()

    # create straight line
    ax.plot([intersect1_x, x1], [intersect1_y, y1], 'b--', label='Trajectory')
    # Create the Arc patch
    # Calculate the start and end angles for the arc
    end_angle= math.degrees(math.atan2(intersect1_y - y_center, intersect1_x - x_center))

    start_angle= end_angle + math.degrees(turning_angle)  # Calculate the end angle based on the turning angle
    print(start_angle)
    # Calculate the angle of the arc
    arc_angle = end_angle - start_angle

    center = (x_center, y_center)
    width = 2 * r
    height = 2 * r

    angle = 0
    arc = patches.Arc(center, width, height, angle=angle, theta1=start_angle, theta2=end_angle, linewidth=1,
                      edgecolor='r', linestyle='--')
    ax.add_patch(arc)
    # # Calculate the start and end angles for the arc
    # start_angle = math.degrees(math.atan2(intersect1_y - y_center, intersect1_x - x_center))
    # # print(start_angle)
    # end_angle = math.degrees(math.atan2(y0 - y_center, x0 - x_center))
    # # print(end_angle)
    # # Calculate the angle of the arc
    # arc_angle = end_angle - start_angle

    # Print the angle of the arc
    print("Angle of the arc: {:.2f} degrees".format(arc_angle))

    center = (x_center, y_center)
    width = 2 * r
    height = 2 * r
    # angle = 0# math.degrees(angle_l_straight_line) #theta_degree + math.degrees(angle_displacement)#
    angle = 90  # theta_degree + math.degrees(angle_displacement)
    arc = patches.Arc(center, width, height, angle=angle, theta1=start_angle, theta2=end_angle, linewidth=1,
                      edgecolor='r',
                      linestyle='--')
    ax.add_patch(arc)

    ax.plot(x0, y0, 'kx', label='Starting Point')
    ax.plot(x1, y1, 'kx', label='End Point')
    ax.plot(x_center, y_center, 'gx', label='Center')

    # Plot an arrow indicating the orientation
    arrow_length = 0.5
    arrow_dx = arrow_length * math.cos(theta)
    arrow_dy = arrow_length * math.sin(theta)
    ax.arrow(x0, y0, arrow_dx, arrow_dy, color='black', width=0.01)

    # Plot the displacement vector
    ax.plot([x0, x1], [y0, y1], color='blue', linestyle='-', linewidth=1)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)  # Set the title
    ax.legend()
    plt.show()
    return

# Define the values
theta_degree = -20
theta = math.radians(theta_degree)

# Adjust the angle to be within [0:2π]
theta = theta % (2 * math.pi)

# Adjust -90 degrees to be equivalent to 270 degrees
if theta < 0:
    theta += 2 * math.pi

# theta_degree = math.degrees(theta)
print(f'theta rad: {theta}, degree: {theta_degree}')

x0 = 0
y0 = 0
x1 = 2
y1 = 2
r = 1

# angle displacement vector
angle_displacement = math.atan((y1 - y0) / (x1 - x0))
print(f'angle_displacement rad:{angle_displacement}, deg: {math.degrees(angle_displacement)}')
print('difference between angle dis vector and theta',abs(theta_degree-math.degrees(angle_displacement)))


def get_quadrant(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if dx > 0 and dy > 0:
        return "Q1"
    elif dx < 0 and dy > 0:
        return "Q2"
    elif dx < 0 and dy < 0:
        return "Q3"
    elif dx > 0 and dy < 0:
        return "Q4"
    elif dx == 0 and dy == 0:
        return "At the origin"
    elif dx == 0:
        if dy > 0:
            return "On the positive y-axis"
        else:
            return "On the negative y-axis"
    elif dy == 0:
        if dx > 0:
            return "On the positive x-axis"
        else:
            return "On the negative x-axis"


if get_quadrant(x0, y0, x1, y1) == "Q1":
    print("Q1")
    if theta == angle_displacement:
        direction = 'forward'
        l_straight_line = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    elif theta == math.pi+angle_displacement:
        direction = 'backwards'
        l_straight_line = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    elif angle_displacement < theta < angle_displacement + math.pi:
        print('normal Q1')
        x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line, turning_angle, \
        angle_l_straight_line = path_finder(theta_degree = theta_degree,
                                            x0 = x0,
                                            y0 = y0,
                                            x1 = x1,
                                            y1 = y1,
                                            r  = r)

        plot_path(theta, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line,
                  turning_angle,
                  angle_l_straight_line,"Path Q1")
    else:  # angle_displacement > theta
        print('mirror displacement vector Q1')
        theta_mirror = angle_displacement - theta + angle_displacement
        theta_mirror_degree = math.degrees(theta_mirror)

        x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line, turning_angle, \
        angle_l_straight_line = path_finder(theta_degree = theta_mirror_degree,
                                            x0 = x0,
                                            y0 = y0,
                                            x1 = x1,
                                            y1 = y1,
                                            r  = r)

        plot_path(theta = theta_mirror,
                  x_center = x_center,
                  y_center = y_center,
                  intersect1_x = intersect1_x ,
                  intersect1_y = intersect1_y,
                  intersect2_x = intersect2_x,
                  intersect2_y = intersect2_y,
                  l_straight_line = l_straight_line,
                  turning_angle = turning_angle,
                  title = "Path Q1 using mirrored orientation")



        reflected_x_center, reflected_y_center, reflected_intersect1_x, reflected_intersect1_y, reflected_intersect2_x, reflected_intersect2_y, l_straight_line, reflected_turning_angle,reflected_angle_l_straight_line = reflect_wrt_displacement(x0, y0, x1, y1, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y,angle_l_straight_line)

        plot_path(theta, reflected_x_center, reflected_y_center,  reflected_intersect1_x, reflected_intersect1_y, reflected_intersect2_x, reflected_intersect2_y, l_straight_line,
                  reflected_turning_angle,
                  reflected_angle_l_straight_line,"Final path Q1 after re-mirroring")


elif get_quadrant(x0, y0, x1, y1) == "Q2":
    print("Q2")
    if theta == angle_displacement:
        direction = 'forward'
        l_straight_line = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    elif theta == math.pi+angle_displacement:
        direction = 'backwards'
        l_straight_line = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    else:
        theta_mirror_yaxis = math.pi - theta
        theta_mirror_yaxis_degree = math.degrees(theta_mirror_yaxis)

        reflected_x1, reflected_y1 = reflect_point_wrt_vertical(x1, y1, x0)

        if theta_mirror_yaxis > angle_displacement:
            x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line, turning_angle, \
                angle_l_straight_line = path_finder(theta_mirror_yaxis_degree, x0, y0, reflected_x1, reflected_y1, r)

            plot_path_wrt_disvector(theta_mirror_yaxis, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line,
                    turning_angle,
                    angle_l_straight_line)

            x_center_reflected_wrt_vertical, y_center_reflected_wrt_vertical, intersect1_x_reflected_wrt_vertical, \
            intersect1_y_reflected_wrt_vertical, intersect2_x_reflected_wrt_vertical, \
            intersect2_y_reflected_wrt_vertical, reflected_angle_l_straight_line \
            = reflect_wrt_vertical(x0, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y,angle_l_straight_line)

            plot_path_wrt_disvector(theta, x_center_reflected_wrt_vertical, y_center_reflected_wrt_vertical, intersect1_x_reflected_wrt_vertical,
                                    intersect1_y_reflected_wrt_vertical, intersect2_x_reflected_wrt_vertical, intersect2_y_reflected_wrt_vertical,
                                    l_straight_line,turning_angle,
                                    reflected_angle_l_straight_line)




        else:  # angle_displacement > theta
            theta_mirror = angle_displacement - theta_mirror_yaxis + angle_displacement
            theta_mirror_degree = math.degrees(theta_mirror)

            x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y, l_straight_line, turning_angle, \
                angle_l_straight_line = path_finder(theta_mirror_degree, x0, y0, reflected_x1, reflected_y1, r)

            plot_path(theta_mirror, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y,
                    l_straight_line,
                    turning_angle,
                    l_straight_line)

            reflected_x_center, reflected_y_center, reflected_intersect1_x, reflected_intersect1_y, reflected_intersect2_x, \
                reflected_intersect2_y, l_straight_line, reflected_turning_angle, reflected_angle_l_straight_line \
                = reflect_wrt_displacement(
                x0, y0, reflected_x1, reflected_y1, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y,
                angle_l_straight_line)

            plot_path(theta_mirror_yaxis, reflected_x_center, reflected_y_center, reflected_intersect1_x,
                                reflected_intersect1_y, reflected_intersect2_x, reflected_intersect2_y, l_straight_line,
                                reflected_turning_angle,
                                reflected_angle_l_straight_line)

            reflected_x_center_reflected_wrt_vertical, reflected_y_center_reflected_wrt_vertical, reflected_intersect1_x_reflected_wrt_vertical, \
                reflected_intersect1_y_reflected_wrt_vertical, reflected_intersect2_x_reflected_wrt_vertical, \
                reflected_intersect2_y_reflected_wrt_vertical, reflected_angle_l_straight_line \
                = reflect_wrt_vertical(x0, x_center, y_center, intersect1_x, intersect1_y, intersect2_x, intersect2_y,
                                       angle_l_straight_line)

            plot_path(theta, reflected_x_center_reflected_wrt_vertical, reflected_y_center_reflected_wrt_vertical,
                                    reflected_intersect1_x_reflected_wrt_vertical,
                                    reflected_intersect1_y_reflected_wrt_vertical, reflected_intersect2_x_reflected_wrt_vertical,
                                    reflected_intersect2_y_reflected_wrt_vertical,
                                    l_straight_line, turning_angle,
                                    reflected_angle_l_straight_line)



