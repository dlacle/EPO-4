
import math
import matplotlib.pyplot as plt
import numpy as np
from check_reachability_endpoint import check_endpoint_reachability
from circle_line_function import circle_line_function

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

def plot_safety_border():
    # Function to plot the blue dotted border
    plt.plot([x_min, x_max, x_max, x_min, x_min],
             [y_min, y_min, y_max, y_max, y_min],
             linestyle='dotted', color='blue')
# Define the field size and safety border distance and grid parameters
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
init_or = -20
init_or = init_or % 360

# start = input('Coordinates of Start (example: [0, 0]): ')
# x_init, y_init = ast.literal_eval(start)
x_init = 300
y_init = 100

# waypoint = input('Coordinates of Waypoint (example: [0, 0]): ')
# w_x, w_y = ast.literal_eval(waypoint)
w_x = 100
w_y = 300

# final = input('Coordinates of Final Destination (example: [0, 0]): ')
# f_x, f_y = ast.literal_eval(final)
f_x = 200
f_y = 300
# radius of circle will be constant assuming steering angle is 35 degrees
r = L / math.sin(math.radians(35))
r = 100
print("Radius:",r)

v1 = [w_x - x_init, w_y - y_init]
v2 = [f_x - w_x, f_y - w_y]
phase_v1 = math.degrees(math.atan2(v1[1], v1[0]))  # Angle displacement vector
phase_v1 = phase_v1 % 360
phase_v2 = math.degrees(math.atan2(v2[1], v2[0]))
phase_v2 = phase_v2 % 360
print('angle displacement vector:', phase_v1)
print('angle displacement vector:', phase_v2)

# init_or = adjust_orientation(init_or,phase_v1)
# init_or = map_orientation(phase_v1,init_or)
print('init_or', init_or)
print('diff', abs(init_or - phase_v1))



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

# initialize the new_or which will be the recursive variable
new_or = init_or
x_start = x_init
y_start = y_init
x_dest = w_x
y_dest = w_y


# check driving in a straight line
if phase_v1 == init_or or phase_v1 == (180 + init_or) % 360:
    l1_lenght, Mdir = straight_line(phase_v1, init_or, x_init, y_init, w_x, w_y)
    print(f'l1_lenght {l1_lenght},Mdir {Mdir}')

elif check_endpoint_reachability(x_init, y_init, new_or, r, w_x, w_y):
    # Execute circle_line_function
    new_or, x_start,y_start,alpha,x_short,y_short,l_r,l1_length = circle_line_function(
        phase_v1, new_or, r, x_init, y_init, x_dest, y_dest)
    print(check_within_field(x_short, y_short, x_min, x_max, y_min, y_max))

    if check_endpoint_reachability(w_x, w_y, new_or, r, f_x, f_y):
        new_or, x_start,y_start,alpha,x_short,y_short,l_r,l1_length = circle_line_function(
        phase_v2, new_or, r, w_x, w_y, f_x, f_y)
        print(check_within_field(x_short, y_short, x_min, x_max, y_min, y_max))
    else:
        print("Second point not reachable")
else:
    print("First point not reachable")


# Plot the field border
plot_safety_border()

# Create a list of microphone coordinates and labels
microphones = [(field_size, 0, 'm1'), (field_size, field_size, 'm2'),
               (0, field_size, 'm3'), (0, 0, 'm4'), (field_size / 2, 0, 'm5')]
# Plot the microphones
for mic in microphones:
    plt.plot(mic[0], mic[1], marker='s', color='blue', markersize=12)
    plt.text(mic[0], mic[1] + 20, mic[2], color='blue', fontsize=12, ha='center')

# Plots the points and the displacement vectors
# Plotting "x" marks at the given locations
plt.plot(x_init, y_init, 'x', color='#0072BD', markersize=10)
plt.plot(w_x, w_y, 'x', color='#0072BD', markersize=10)
plt.plot(f_x, f_y, 'x', color='#0072BD', markersize=10)

# Plotting the displacement vectors
arrow_width = 0.8  # Adjust the width of the arrows
plt.arrow(x_init, y_init, w_x - x_init, w_y - y_init, color='red', width=arrow_width,
          length_includes_head=True)
plt.arrow(w_x, w_y, f_x - w_x, f_y - w_y, color='blue', width=arrow_width,
          length_includes_head=True)

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

