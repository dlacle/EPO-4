import matplotlib.pyplot as plt
import math

# Define the values
initial_orientation = 90
start_posx = 1
start_posy = 1
end_posx = 5
end_posy = 2
max_forward_radius = 1
max_backwards_radius = 1

# Calculate the center of the first circle
x_center = start_posx + max_forward_radius * math.cos(math.radians(initial_orientation - 90))
y_center = start_posy + max_forward_radius * math.sin(math.radians(initial_orientation - 90))

# Calculate the length of the line
displacement_vector = math.sqrt((x_center - end_posx) ** 2 + (y_center - end_posy) ** 2)
l_straight_line = math.sqrt(displacement_vector ** 2 - max_forward_radius ** 2)

# Create the figure and axes
fig, ax = plt.subplots()

# Plot the first circle with a dashed line
circle1 = plt.Circle((x_center, y_center), max_backwards_radius, edgecolor='black', facecolor='none', linestyle='--')
ax.add_artist(circle1)

# Plot the second circle with a dashed line
circle2 = plt.Circle((end_posx, end_posy), l_straight_line, edgecolor='r', facecolor='none', linestyle='--')
ax.add_artist(circle2)

# Plot the center of the circles
ax.plot(x_center, y_center, marker='o', color='black', markersize=3)
ax.plot(end_posx, end_posy, marker='x', color='black', markersize=5)

# Plot the line connecting the centers
ax.plot([x_center, end_posx], [y_center, end_posy], color='black', linestyle='--', linewidth=1)

# Plot an 'x' marker at the start position
ax.plot(start_posx, start_posy, marker='x', color='black', markersize=5)

# Plot an arrow indicating the orientation
arrow_length = 0.5
arrow_dx = arrow_length * math.cos(math.radians(initial_orientation))
arrow_dy = arrow_length * math.sin(math.radians(initial_orientation))
ax.arrow(start_posx, start_posy, arrow_dx, arrow_dy, color='black', width=0.01)

# Plot the displacement vector
ax.plot([start_posx, end_posx], [start_posy, end_posy], color='blue', linestyle='-', linewidth=1)



# Find the intersection points
intersection_dist = math.sqrt((end_posx - x_center) ** 2 + (end_posy - y_center) ** 2)
alpha = math.acos(
    (max_forward_radius ** 2 + intersection_dist ** 2 - l_straight_line ** 2) / (2 * max_forward_radius * intersection_dist))
beta = math.atan2(end_posy - y_center, end_posx - x_center)
theta1 = beta + alpha
theta2 = beta - alpha

# Calculate the intersection points
intersect1_x = x_center + max_forward_radius * math.cos(theta1)
intersect1_y = y_center + max_forward_radius * math.sin(theta1)
intersect2_x = x_center + max_forward_radius * math.cos(theta2)
intersect2_y = y_center + max_forward_radius * math.sin(theta2)

# Print the intersection points
print("Intersection Point 1: ({:.2f}, {:.2f})".format(intersect1_x, intersect1_y))
print("Intersection Point 2: ({:.2f}, {:.2f})".format(intersect2_x, intersect2_y))

# Plot the intersection points
ax.plot(intersect1_x, intersect1_y, marker='o', color='black', markersize=3)

# Plot a dotted line between intersection1 and end_posx, end_posy
ax.plot([intersect1_x, end_posx], [intersect1_y, end_posy], color='black', linestyle='--', linewidth=1)

# Set the aspect ratio to equal to avoid distortion
ax.set_aspect('equal')

# Turn off axis numbering
ax.axis('off')

# Set the axis limits based on the coordinates
ax.set_xlim(min(start_posx, end_posx) - max_forward_radius - 2, max(start_posx, end_posx) + max_forward_radius + 2)
ax.set_ylim(min(start_posy, end_posy) - max_forward_radius - 2, max(start_posy, end_posy) + max_forward_radius + 2)
# # Set the arrowhead style
# arrowhead_style = {'arrowstyle': '->'}
#
# # Plot the arrowheads for the x and y axes
# ax.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=arrowhead_style)
# ax.annotate("", xy=(0, 1), xytext=(0, 0), arrowprops=arrowhead_style)
#
# # Add labels to the arrowheads
# ax.text(1.05, 0, 'x-axis', ha='center', va='center')
# ax.text(0, 1.05, 'y-axis', ha='center', va='center')

# Show the plot
plt.show()
