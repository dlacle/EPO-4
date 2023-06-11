import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.axisartist.axislines import SubplotZero

L = 34.5

# radius of circle will be constant assuming the steering angle is 35 degrees
r = L / math.sin(math.radians(35))
r = 100
print("Radius:", r)

center_x = 200  # x-coordinate of the center (half of the axis dimension)
center_y = 200  # y-coordinate of the center (half of the axis dimension)

fig = plt.figure(figsize=(6, 6))  # Set the figure size to match the desired axis dimensions
ax = SubplotZero(fig, 111)
fig.add_subplot(ax)

for direction in ["xzero", "yzero"]:
    # adds arrows at the ends of each axis
    ax.axis[direction].set_axisline_style("-|>")
    # adds X and Y-axis from the origin
    ax.axis[direction].set_visible(True)

for direction in ["left", "right", "bottom", "top"]:
    # hides borders
    ax.axis[direction].set_visible(False)

x = np.zeros(360)
y = np.zeros(360)

# Generate the whole circle
for theta in range(1, 361):  # in degrees
    x[theta - 1] = r * np.cos(np.deg2rad(theta)) + center_x
    y[theta - 1] = r * np.sin(np.deg2rad(theta)) + center_y

alpha = 2.149474931288235
new_or = 135
# x_short = x[int(np.mod(np.abs(90 + new_or - np.round(np.rad2deg(alpha))), 360)):int(np.mod(np.abs(90 + new_or), 360))]
# y_short = y[int(np.mod(np.abs(90 + new_or - np.round(np.rad2deg(alpha))), 360)):int(np.mod(np.abs(90 + new_or), 360))]
# new_or = new_or - np.round(np.rad2deg(alpha))

x_short = x[int(np.mod(np.abs(180 + new_or), 360)):int(np.mod(np.abs(180 + new_or + np.round(np.rad2deg(alpha))), 360))]
y_short = y[int(np.mod(np.abs(180 + new_or), 360)):int(np.mod(np.abs(180 + new_or + np.round(np.rad2deg(alpha)))), 360)]
new_or = new_or + np.round(np.rad2deg(alpha))

# Plot the circle
x_short = x_short.flatten() #reshapes x_short into a column vector
y_short = y_short.flatten() #reshapes x_short into a column vector
plt.plot(x_short, y_short, 'r--')
# ax.plot(x, y)
ax.axis([0, 480, 0, 480])  # Set the axis limits to match the desired dimensions
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Circle')
ax.grid(True)
plt.show()

plt.show()