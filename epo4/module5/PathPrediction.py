import math

# Define the values
# initial_orientation
theta_degree = 0
theta = math.radians(theta_degree)

# initial steering angle
phi = 90

# Starting point
x0 = 1
y0 = 1

# end point
x1 = 4
y1 = 4

# forward_radius
r = 2
# max_backwards_radius = 1

# Calculate the center of the first circle
x_center = x0 + r * math.cos(math.radians(theta - 90))
y_center = y0 + r * math.sin(math.radians(theta - 90))

# Calculate the length of the line
center_to_destination = math.sqrt((x_center - x1) ** 2 + (y_center - y1) ** 2)
angle_displacement_vector = math.atan((x1 - x0) / (y1 - y0))
l_straight_line = math.sqrt(center_to_destination ** 2 - r ** 2)

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

begin_to_intercept = math.sqrt(
    (x0 - intersect1_x) ** 2 + (y0 - intersect1_y) ** 2)  # length vector start point-intersection circle
turning_angle = 2 * math.asin(begin_to_intercept / 2 * r)  # simplified and her written function of the cosign law
print(turning_angle)

# Calculate the position (x,y) and the angle of the car at given point on the trajectory:
# i_max = 1000
# for i = 1:i_max:
#     x_trajectory[i]

# Calculate the angle of the car at the final position:
