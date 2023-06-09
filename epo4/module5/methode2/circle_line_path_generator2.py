
import math
import matplotlib.pyplot as plt
import numpy as np
from check_reachability_endpoint import check_endpoint_reachability
from circle_line_funcion2 import circle_line_function

def check_within_field(x_short, y_short, x_min, x_max, y_min, y_max):
    for x, y in zip(x_short, y_short):
        if not (x_min <= x <= x_max and y_min <= y <= y_max):
            return False
    return True

def straight_line(phase_v, new_or, x_start, y_start, x_dest, y_dest):
    l1_lenght = math.sqrt((x_dest - x_start) ** 2 + (y_dest - y_start) ** 2)
    if phase_v == new_or:
        print('orientation same direction as displacement, drive forward')
        Mdir = 'forward'

    else:  # phase_v == -new_or
        print('orientation opposite direction as displacement, drive backwards')
        Mdir = 'backwards'

    return l1_lenght, Mdir

def plot_safety_border(x_min,x_max,y_min,y_max):
    # Function to plot the blue dotted border
    plt.plot([x_min, x_max, x_max, x_min, x_min],
             [y_min, y_min, y_max, y_max, y_min],
             linestyle='dotted', color='blue')

# def circle_line_path_generator(r_f,r_b):
# Define the field size and safety border distance and grid parameters
r_f = 100
r_b = 80
field_size = 480
grid_spacing = 30
axis_spacing = 60
safety_border_distance = 26

# Define the field boundaries
x_min = safety_border_distance
x_max = field_size - safety_border_distance
y_min = safety_border_distance
y_max = field_size - safety_border_distance

# Assuming max steering angle is 35 degrees in both directions
L = 34.5  # Length of the car in cm's
# init_or = float(input('Give the initial orientation (angle to positive x-axis): '))
init_or = 135
init_or = init_or % 360

# start = input('Coordinates of Start (example: [0, 0]): ')
# x_init, y_init = ast.literal_eval(start)
x_init = 30
y_init = 30

# waypoint = input('Coordinates of Waypoint (example: [0, 0]): ')
# w_x, w_y = ast.literal_eval(waypoint)
w_x = 200
w_y = 200

# final = input('Coordinates of Final Destination (example: [0, 0]): ')
# f_x, f_y = ast.literal_eval(final)
f_x = 200
f_y = 300
location_targets = [[x_init,y_init],[w_x,w_y]]#,[f_x,f_y],[420,60]

phase_displacements = []

for i in range(1, len(location_targets)):
    dis_vect = [location_targets[i][0] - location_targets[i - 1][0], location_targets[i][1] - location_targets[i - 1][1]]
    phase_dis_vect = math.degrees(math.atan2(dis_vect[1], dis_vect[0]))  # Angle displacement vector
    phase_dis_vect = phase_dis_vect % 360
    phase_displacements.append(phase_dis_vect)

# print('init_or', init_or)
# print('diff', abs(init_or - phase_v1))



# Create a square figure
fig = plt.figure(figsize=(6, 6))
plt.ion()

"""

the method used only works if the v vector has a positive x and y component.
In the cases it doesn't, we mirror the destination point with respect to the
appropriate axis going through the start point to create an imaginary image destination
(don't forget to mirror the orientation too). After we make the image
destination, we pathfind to the image destination. Then we mirror the path
we found again to get the needed path.
"""

l1_length = []
Mdir = []
alpha = []
orientation = [init_or]
l_r = []

for i in range(len(location_targets) - 1):
    x_start, y_start = location_targets[i]
    x_dest, y_dest = location_targets[i + 1]

    # Plot an arrow indicating the orientation
    arrow_length = 34.5
    arrow_dx = arrow_length * np.cos(np.deg2rad(orientation[-1]))
    arrow_dy = arrow_length * np.sin(np.deg2rad(orientation[-1]))
    plt.arrow(x_start, y_start, arrow_dx, arrow_dy, color='black', width=0.8)

    print(f"Starting point: ({x_start}, {y_start}), Destination point: ({x_dest}, {y_dest})")

    if phase_displacements[i] == orientation[-1] or phase_displacements[i] == (180 + orientation[-1]) % 360:
        l1_length_res, Mdir_res = straight_line(phase_displacements[i], orientation[-1], x_start, y_start, x_dest, y_dest)
        alpha_res = 0
        l1_length.append(l1_length_res)
        Mdir.append(Mdir_res)
        alpha.append(alpha_res)
        orientation.append(init_or)
        l_r.append(None)
        print("No turn needed, drive straight")
        print(f'l1_length {l1_length_res}, Mdir {Mdir_res}')

    elif check_endpoint_reachability(x_start, y_start, orientation[-1], r_f, x_dest, y_dest):
        while True:
            new_or_res, x_start_res, y_start_res, alpha_res, x_short_res, y_short_res, l_r_res,l1_length_res,intersect, center_x, center_y= circle_line_function(
                phase_displacements[i], orientation[-1], r_f, x_start, y_start, x_dest, y_dest)
            if not check_within_field(x_short_res, y_short_res, x_min, x_max, y_min, y_max):
                print('Driving forward to new point, point reachable but outside safety border, trying backwards')
                if check_endpoint_reachability(x_start, y_start, ((orientation[-1] + 180) % 360), r_b, x_dest, y_dest): #check if backwards turn is possible
                    print('Driving backwards to new point, point is reachable, check if within safety border')
                    new_or_res, x_start_res, y_start_res, alpha_res, x_short_res, y_short_res, l_r_res,l1_length_res,intersect, center_x, center_y = circle_line_function(
                        phase_displacements[i],((orientation[-1] + 180) % 360), r_f, x_start, y_start, x_dest, y_dest)
                    new_or_res = ((new_or_res + 180) % 360) # change back to correct orient
                    if check_within_field(x_short_res, y_short_res, x_min, x_max, y_min, y_max):
                        # use the parameters of the function above
                        l1_length.append(l1_length_res)
                        alpha.append(alpha_res)
                        orientation.append(new_or_res)
                        l_r.append(l_r_res)

                        Mdir_res = 'backwards'
                        Mdir.append(Mdir_res)

                        #plot the path
                        plt.plot(x_short_res, y_short_res, color='blue', linestyle='--')  # plot turn
                        plt.plot([x_dest, x_short_res[0]], [y_dest, y_short_res[0]],color='black', linestyle='--')  # plot straigtline

                        # plotting points
                        plt.plot(intersect[0], intersect[1], marker='o', color='black', markersize=5)
                        plt.plot(center_x, center_y, marker='x', color='green', markersize=10)

                        print('Driving backwards to new point, point reachable and within safety border')
                        break

                    else:
                        print('points never reachable forward and backwards, dead point')
                        break

            else:
                print('Driving forward to new point, point reachable and within safety border')
                Mdir_res = 'forward'
                Mdir.append(Mdir_res)
                l1_length.append(l1_length_res)
                alpha.append(alpha_res)
                orientation.append(new_or_res)
                l_r.append(l_r_res)

                # plot the path
                plt.plot(x_short_res, y_short_res, 'r--')  # plot turn
                plt.plot([x_dest, x_short_res[0]], [y_dest, y_short_res[0]], 'g--')  # plot straigtline

                # plotting points
                plt.plot(intersect[0], intersect[1], marker='o', color='black', markersize=5)
                plt.plot(center_x, center_y, marker='x', color='green', markersize=10)
                break

    elif check_endpoint_reachability(x_start, y_start, ((orientation[-1] + 180) % 360), r_b, x_dest, y_dest):
        print('Point inside turn radius forwards, backwards turn possible, checking safety border')
        while True:
            new_or_res, x_start_res, y_start_res, alpha_res, x_short_res, y_short_res, l_r_res,l1_length_res,intersect, center_x, center_y = circle_line_function(
                phase_displacements[i], ((orientation[-1] + 180) % 360), r_f, x_start, y_start, x_dest, y_dest)
            new_or_res = ((new_or_res + 180) % 360)
            if check_within_field(x_short_res, y_short_res, x_min, x_max, y_min, y_max):
                print('Point inside turn radius forwards, but backwards possible, inside safety border')
                # use the parameters of the function above
                l1_length.append(l1_length_res)
                alpha.append(alpha_res)
                orientation.append(new_or_res)
                l_r.append(l_r_res)

                Mdir_res = 'backwards'
                Mdir.append(Mdir_res)

                # plot the path
                plt.plot(x_short_res, y_short_res, color='blue', linestyle='--')  # plot turn
                plt.plot([x_dest, x_short_res[0]], [y_dest, y_short_res[0]],color='black', linestyle='--')  # plot straigtline

                # plotting points
                plt.plot(intersect[0], intersect[1], marker='o', color='black', markersize=5)
                plt.plot(center_x, center_y, marker='x', color='green', markersize=10)
                break
            else:
                print('points never reachable forward and backwards, dead point')
                break
    else:
        print('points not reachable forward and backwards, try something else')

# for i in range(len(location_targets) - 1):
#     x_start, y_start = location_targets[i]
#     x_dest, y_dest = location_targets[i + 1]
#
#     if phase_displacements[i] == new_or or phase_displacements[i] == (180 + new_or) % 360:
#         l1_length, Mdir = straight_line(phase_displacements[i], new_or, x_start, y_start, x_dest, y_dest)
#         print("No turn neeeded drive straight")
#         print(f'l1_length {l1_length}, Mdir {Mdir}')
#
#     elif check_endpoint_reachability(x_start, y_start, new_or, r_f, x_dest, y_dest) == True:
#         Mdir = 'forward'
#         new_or_res, x_start_res, y_start_res, alpha_res, x_short_res, y_short_res, l_r_res,_,_,_,_ = circle_line_function(
#             phase_displacements[i], new_or, r_f, x_start, y_start, x_dest, y_dest)
#         if check_within_field(x_short, y_short, x_min, x_max, y_min, y_max) == False:
#             print('driving forward to new point, point reachable but outside safety border, try backwards')
#             if check_endpoint_reachability(x_start, y_start, ((new_or+180)%360), r_b, x_dest, y_dest) == True:
#                 Mdir = 'backwards'
#                 new_or_res, x_start_res, y_start_res, alpha_res, x_short_res, y_short_res, l_r_res,_,_,_,_ = circle_line_function(
#                 phase_displacements[i], new_or, r_f, x_start, y_start, x_dest, y_dest)
#                 new_or_res = ((new_or_res+180)%360)
#                 if check_within_field(x_short_res, y_short_res, x_min, x_max, y_min, y_max) == True:
#                     # use the parameters of the function above
#                     new_or = new_or_res
#                     alpha = alpha_res
#                     l_r = l_r_res
#                 print('driving backwards to new point, point reachable and within safety border')
#         else:
#             print('driving forward to new point, point reachable and within safety border')
#             new_or =new_or_res
#             alpha = alpha_res
#             l_r = l_r_res
#
#
#     elif check_endpoint_reachability(x_start, y_start, ((new_or+180)%360), r_b, x_dest, y_dest) == True:
#         print('point inside turn radius forwards, but backwards possible, check safety border')
#         Mdir = 'backwards'
#         new_or_res, x_start_res, y_start_res, alpha_res, x_short_res, y_short_res, l_r_res,_,_,_,_ = circle_line_function(
#             phase_displacements[i], new_or, r_f, x_start, y_start, x_dest, y_dest)
#         new_or_res = ((new_or_res + 180) % 360)
#         if check_within_field(x_short_res, y_short_res, x_min, x_max, y_min, y_max) == True:
#             print('point inside turn radius forwards, but backwards possible, inside safety border')
#             # use the parameters of the function above
#             new_or = new_or_res
#             alpha = alpha_res
#             l_r = l_r_res
#     else:
#         print('point not reachable forward and backwards turn, try something else ')

# Plot the field border
plot_safety_border(x_min,x_max,y_min,y_max)

# Create a list of microphone coordinates and labels
microphones = [(field_size, 0, 'm1'), (field_size, field_size, 'm2'),
               (0, field_size, 'm3'), (0, 0, 'm4'), (field_size / 2, 0, 'm5')]
# Plot the microphones
for mic in microphones:
    plt.plot(mic[0], mic[1], marker='s', color='blue', markersize=12)
    plt.text(mic[0], mic[1] + 20, mic[2], color='blue', fontsize=12, ha='center')

# Generate a list of colors for the displacement vectors
colors = plt.cm.viridis(np.linspace(0, 1, len(location_targets) - 1))

# Plotting the points
for point in location_targets:
    plt.plot(point[0], point[1], 'x', color='#0072BD', markersize=10)

# Plotting the displacement vectors with different colors
arrow_width = 0.8  # Adjust the width of the arrows
for i in range(1, len(location_targets)):
    start_point = location_targets[i - 1]
    end_point = location_targets[i]
    displacement_vector = [end_point[0] - start_point[0], end_point[1] - start_point[1]]
    color = colors[i - 1]
    plt.arrow(start_point[0], start_point[1], displacement_vector[0], displacement_vector[1],
              color=color, width=arrow_width, length_includes_head=True)

    # Set grid lines and labels
plt.xticks([i for i in range(0, field_size + 1, grid_spacing)])
plt.yticks([i for i in range(0, field_size + 1, grid_spacing)])
plt.xticks([i for i in range(0, field_size + 1, axis_spacing)], minor=False)
plt.yticks([i for i in range(0, field_size + 1, axis_spacing)], minor=False)
plt.grid(True, linestyle='--', linewidth=0.5, which='both')
plt.grid(True, linestyle='-', linewidth=1, which='major')

# Set the axis limits
plt.xlim(0, field_size)
plt.ylim(0, field_size)
# plt.gca().invert_xaxis()

# add label axis
plt.xlabel("x")
plt.ylabel("y")
# plt.gca().yaxis.set_label_position('right')

# Move the y-axis to the right side
# plt.gca().yaxis.tick_right()

# Set the aspect ratio
plt.gca().set_aspect('equal', adjustable='box')
# plt.savefig('generated_path3.svg', format='svg')
plt.show()
    # return orientation, alpha, l_r, Mdir,l1_lenght

# l1_length.append(l1_length_res)
#                 Mdir.append(Mdir_res)
#                 alpha.append(alpha_res)
#                 orientation.append(new_or_res)
#                 l_r.append(l_r_res)
#
#                 Mdir_res = 'backwards'
#                 Mdir.append(Mdir_res)