import math
import numpy as np
from matplotlib import pyplot as plt

def ObstacleAvoidance(current_location, orientation, dest):
    # calculate the center point of the most probable obstacle location
    location_object = [current_location[0] + 105 * math.cos(math.radians(orientation)),
                       current_location[1] + 105 * math.sin(math.radians(orientation))]

    # displacement vector = line between actual location and destination
    dis_vect = [dest[0] - current_location[0], dest[1] - current_location[1]]

    # angle of this line
    phase_dis = np.arctan2(dis_vect[1], dis_vect[0])
    phase_dis = np.rad2deg(phase_dis)
    phase_dis = phase_dis % 360

    # detect if car is turning clockwise around the center of the field or not
    if (0 < orientation < 180 and current_location[0] > 240) or (180 < orientation < 360 and current_location[0] < 240):
        TurningClockwise = 1
    else:
        TurningClockwise = 0

    # if obstacle more than 1 meter from the border, turning can be done in the most efficient direction
    if (100 < location_object[0] < 380) and (100 < location_object[1] < 380):
        # turn around obstacle counterclockwise
        if orientation < phase_dis:
            Middle = [location_object[0] + 90 * math.cos(math.radians(phase_dis - 90)),
                      location_object[1] + 90 * math.sin(math.radians(phase_dis - 90))]
            Waypoint1 = [location_object[0] + 90 * math.cos(math.radians(phase_dis - 135)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis - 135))]
            Waypoint2 = [location_object[0] + 90 * math.cos(math.radians(phase_dis - 45)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis - 45))]
        # turn around obstacle clockwise
        elif orientation > phase_dis:
            Middle = [location_object[0] + 90 * math.cos(math.radians(phase_dis + 90)),
                      location_object[1] + 90 * math.sin(math.radians(phase_dis + 90))]
            Waypoint1 = [location_object[0] + 90 * math.cos(math.radians(phase_dis + 135)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis + 135))]
            Waypoint2 = [location_object[0] + 90 * math.cos(math.radians(phase_dis + 45)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis + 45))]
    # if too close to the border, drive around from the inside of the field
    else:
        # if KITT drives clockwise, turn around by the left side of the obstacle
        if TurningClockwise:
            Middle = [location_object[0] + 90 * math.cos(math.radians(phase_dis - 90)),
                      location_object[1] + 90 * math.sin(math.radians(phase_dis - 90))]
            Waypoint1 = [location_object[0] + 90 * math.cos(math.radians(phase_dis - 135)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis - 135))]
            Waypoint2 = [location_object[0] + 90 * math.cos(math.radians(phase_dis - 45)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis - 45))]
        # else, turn by the right side
        else:
            Middle = [location_object[0] + 90 * math.cos(math.radians(phase_dis + 90)),
                      location_object[1] + 90 * math.sin(math.radians(phase_dis + 90))]
            Waypoint1 = [location_object[0] + 90 * math.cos(math.radians(phase_dis + 135)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis + 135))]
            Waypoint2 = [location_object[0] + 90 * math.cos(math.radians(phase_dis + 45)),
                         location_object[1] + 90 * math.sin(math.radians(phase_dis + 45))]

    xpoint1 = Waypoint1[0]
    ypoint1 = Waypoint1[1]
    xpoint2 = Waypoint2[0]
    ypoint2 = Waypoint2[1]
    xpoint3 = Middle[0]
    ypoint3 = Middle[1]

    return xpoint1, ypoint1, xpoint2, ypoint2, xpoint3, ypoint3, location_object

current_location = [100, 100]
orientation = 45
dest = [300, 200]

# Call the ObstacleAvoidance function
xpoint1, ypoint1, xpoint2, ypoint2, xpoint3, ypoint3, location_object = ObstacleAvoidance(current_location, orientation, dest)

# Print the points
print("location obstacle: ", location_object)
print("Waypoint 1: ({}, {})".format(xpoint1, ypoint1))
print("Waypoint 2: ({}, {})".format(xpoint2, ypoint2))
print("Middle Point: ({}, {})".format(xpoint3, ypoint3))

# Plotting the field
field_size = 480

# Plot an arrow indicating the orientation
arrow_length = 34.5
arrow_dx = arrow_length * np.cos(np.deg2rad(orientation))
arrow_dy = arrow_length * np.sin(np.deg2rad(orientation))
plt.arrow(current_location[0], current_location[1], arrow_dx, arrow_dy, color='black', width=0.8)

# Plotting the points and location_object
plt.scatter(xpoint1, ypoint1, marker='x', color='blue', label='X1')
plt.scatter(xpoint2, ypoint2, marker='x', color='blue', label='X2')
plt.scatter(xpoint3, ypoint3, marker='x', color='blue', label='X3')
plt.scatter(location_object[0], location_object[1], marker='o', color='red', label='Object')

# Adding labels to points
plt.text(xpoint1, ypoint1, 'X1', ha='right', va='bottom', color='blue')
plt.text(xpoint2, ypoint2, 'X2', ha='right', va='bottom', color='blue')
plt.text(xpoint3, ypoint3, 'X3', ha='right', va='bottom', color='blue')

# Plotting the circle
circle = plt.Circle(location_object, 90, edgecolor='black', facecolor='none')

# Plotting the rectangle
rectangle_width = 40
rectangle_height = 80
rectangle_x = location_object[0] - rectangle_width / 2
rectangle_y = location_object[1] - rectangle_height / 2
rectangle = plt.Rectangle((rectangle_x, rectangle_y), rectangle_width, rectangle_height,
                          edgecolor='green', facecolor='none')

# Setting up the plot
plt.xlim(0, field_size)
plt.ylim(0, field_size)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Obstacle Avoidance')
plt.legend()

# Adding the circle and rectangle to the plot
plt.gca().add_patch(circle)
plt.gca().add_patch(rectangle)

# Display the plot
plt.show()
