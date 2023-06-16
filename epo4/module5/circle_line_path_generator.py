import ast
import math
import matplotlib.pyplot as plt
import numpy as np
from check_reachability_endpoint import check_endpoint_reachability
from circle_line_function import circle_line_function
# def map_orientation(phase_v,orientation):
#     if orientation >= 0:
#         mapped_orientation = orientation % 360
#         if mapped_orientation > phase_v: #180
#             mapped_orientation -= 360
#     else:
#         mapped_orientation = (orientation % 360) - 360
#         if mapped_orientation < -phase_v: #-180
#             mapped_orientation += 360
#     return mapped_orientation
# def adjust_orientation(orientation, phase_v):
#     if orientation < phase_v and orientation > phase_v + 180:
#         return orientation
#     else:
#         return -1 * orientation

# Assuming max steering angle is 35 degrees in both directions
L = 34.5  # Length of the car in cm's
# init_or = float(input('Give the initial orientation (angle to positive x-axis): '))
init_or = 90
init_or = init_or % 360


# start = input('Coordinates of Start (example: [0, 0]): ')
# x_init, y_init = ast.literal_eval(start)
x_init = 300
y_init = 300

# waypoint = input('Coordinates of Waypoint (example: [0, 0]): ')
# w_x, w_y = ast.literal_eval(waypoint)
w_x = 100
w_y = 100

# final = input('Coordinates of Final Destination (example: [0, 0]): ')
# f_x, f_y = ast.literal_eval(final)
f_x = 400
f_y = 360
v1 = [w_x - x_init, w_y - y_init]
v2 = [f_x - w_x, f_y - w_y]
phase_v1 = math.degrees(math.atan2(v1[1], v1[0]))  # Angle displacement vector
phase_v1 = phase_v1 % 360
phase_v2 = math.degrees(math.atan2(v2[1], v2[0]))
print('angle displacement vector:', phase_v1)

# init_or = adjust_orientation(init_or,phase_v1)
# init_or = map_orientation(phase_v1,init_or)
print('init_or',init_or)
print('diff',abs(init_or-phase_v1))

def straight_line(phase_v,new_or, x_start,y_start,x_dest,y_dest):
    l1_lenght = math.sqrt((x_dest - x_start) ** 2 + (y_dest - y_start) ** 2)
    if phase_v == new_or:
        print('orientation same direction as displacement, drive forward')
        Mdir = 'forward'

    else: # phase_v == -new_or
        print('orientation opposite direction as displacement, drive backwards')
        Mdir = 'backwards'

    return l1_lenght,Mdir

#check driving in a straight line
if phase_v1 == init_or or phase_v1 == (180+init_or)%360:
    l1_lenght, Mdir = straight_line(phase_v1, init_or, x_init, y_init, w_x, w_y)
    print(f'l1_lenght {l1_lenght},Mdir {Mdir}')

else:

    # if v1[0] < 0:
    #     print('test')
    #     phase_v1 += 180
    # if v2[0] < 0:
    #     phase_v2 += 180

    # Create a square figure
    fig = plt.figure(figsize=(6, 6))
    plt.ion()

    # Plots the points and the displacement vectors
    # Plotting "x" marks at the given locations
    plt.plot(x_init, y_init, 'x', color='#0072BD', markersize=10)
    plt.plot(w_x, w_y, 'x', color='#0072BD', markersize=10)
    plt.plot(f_x, f_y, 'x', color='#0072BD', markersize=10)

    # Plotting the displacement vectors
    arrow_width = 0.8 # Adjust the width of the arrows
    plt.arrow(x_init, y_init, w_x - x_init, w_y - y_init, color='red', width=arrow_width,
              length_includes_head=True)
    # plt.arrow(w_x, w_y, f_x - w_x, f_y - w_y, color='blue', width=arrow_width,
    #           length_includes_head=True)


    # if angle between v and destination is smaller than or equal to 90 degrees
    # we can use a single circle line path. If it is larger, we have to make an
    # imaginary waypoint to do a quarter circle first, then do circle line
    #
    # the method used only works if the v vector has a positive x and y component.
    # In the cases it doesn't, we mirror the destination point with respect to the
    # appropriate axis going through the start point to create an imaginary image destination
    # (don't forget to mirror the orientation too). After we make the image
    # destination, we pathfind to the image destination. Then we mirror the path
    # we found again to get the needed path.

    # initialize the new_or which will be the recursive variable
    new_or = init_or
    x_start = x_init
    y_start = y_init
    x_dest = w_x
    y_dest = w_y

    # radius of circle will be constant assuming steering angle is 35 degrees
    r = L / math.sin(math.radians(35))
    r = 100
    # print("Radius:",r)

    if check_endpoint_reachability(x_init, y_init, new_or, r, w_x, w_y):
        # Execute circle_line_function
        new_or,x_start,y_start,alpha,_,_,l_r,x_mirror,y_mirror,both_mirror,l1_vector = circle_line_function(phase_v1, new_or,r,x_init,y_init,x_dest,y_dest)

        # Calculate the angle in degrees
        final_angle = np.degrees(np.arctan2(l1_vector[1], l1_vector[0]))
        print('final_angle:',final_angle)

        # if check_endpoint_reachability(w_x, w_y, final_angle, r, f_x, f_y):
        #     new_or, x_start, y_start, alpha, _, _, l_r, x_mirror, y_mirror, both_mirror, l1_vector = circle_line_function(
        #         phase_v2, final_angle, r, w_x, w_y, f_x, f_y)
        # else:
        #     print("Second point not reachable")
    else:
        print("First point not reachable")

    # Set the axis limits
    plt.xlim(0, 500)
    plt.ylim(0, 500)

    # Set the aspect ratio
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.savefig('generated_path3.svg', format='svg')
    plt.show()
