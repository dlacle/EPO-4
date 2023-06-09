import ast
import math
import matplotlib.pyplot as plt
import numpy as np

from circle_line_function import circle_line_function

# Assuming max steering angle is 35 degrees in both directions
L = 34.5  # Length of the car in cm's
# init_or = float(input('Give the initial orientation (angle to positive x-axis): '))
init_or = 335
# start = input('Coordinates of Start (example: [0, 0]): ')
# x_init, y_init = ast.literal_eval(start)
x_init = 400
y_init = 400
# This should draw things in the GUI
# waypoint = input('Coordinates of Waypoint (example: [0, 0]): ')
# w_x, w_y = ast.literal_eval(waypoint)
w_x = 300
w_y = 300

# final = input('Coordinates of Final Destination (example: [0, 0]): ')
# f_x, f_y = ast.literal_eval(final)
f_x = 250
f_y = 200
v1 = [w_x - x_init, w_y - y_init]
v2 = [f_x - w_x, f_y - w_y]
phase_v1 = math.degrees(math.atan2(v1[1], v1[0]))  # Angle displacement vector
phase_v2 = math.degrees(math.atan2(v2[1], v2[0]))

if v1[0] < 0:
    phase_v1 += 180
if v2[0] < 0:
    phase_v2 += 180

plt.axis('equal')
plt.ion()

# Plots the points and the displacement vectors
# Plotting "x" marks at the given locations
plt.plot(x_init, y_init, 'x', color='#0072BD', markersize=10)
plt.plot(w_x, w_y, 'x', color='#0072BD', markersize=10)
plt.plot(f_x, f_y, 'x', color='#0072BD', markersize=10)

# Plotting the displacement vectors
plt.arrow(x_init, y_init, w_x - x_init, w_y - y_init, color='red', width=0.02, length_includes_head=True)
plt.arrow(w_x, w_y, f_x - w_x, f_y - w_y, color='blue', width=0.02, length_includes_head=True)


# if angle between v and destination is smaller than or equal to 90 degrees
# we can use a single circle line path. If it is larger, we have to make an
# imaginary waypoint to do a quarter circle first, then do circle line

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
print("Radius:",r)

new_or,x_start,y_start,alpha,_,_,l_r,x_mirror,y_mirror,both_mirror,l1_vector = circle_line_function(phase_v1, new_or,r,x_init,y_init,x_dest,y_dest)

# Calculate the angle in degrees
final_angle = np.degrees(np.arctan2(l1_vector[1], l1_vector[0]))
print(final_angle)

# new_or,x_start,y_start,alpha,_,_,l_r,x_mirror,y_mirror,both_mirror = circle_line_function(phase_v2, final_angle,r,w_x,w_y,f_x,f_y)
# Set the axis limits
# plt.axis([0, 480, 0, 480])
plt.show()