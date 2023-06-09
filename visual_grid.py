import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

import numpy as np


def visuel_grid():#starting_x, starting_y, orientation, waypoint_x, waypoint_y, end_x, end_y
    # Create the figure and axes
    fig, ax = plt.subplots()

    # Define the field dimensions and grid parameters
    field_size = 480
    grid_spacing = 30
    axis_spacing = 60

    # Set the axis limits
    ax.set_xlim(0, field_size)
    ax.set_ylim(0, field_size)
    ax.invert_xaxis()

    # Create a list of microphone coordinates and labels
    microphones = [(field_size, 0, 'm1'), (field_size, field_size, 'm2'),
                   (0, field_size, 'm3'), (0, 0, 'm4'), (field_size/2, 0, 'm5')]

    # Plot the microphones
    for mic in microphones:
        ax.plot(mic[0], mic[1], marker='s', color='blue', markersize=12)
        ax.text(mic[0], mic[1]+20, mic[2], color='blue', fontsize=12, ha='center')

    # Generate a random source location
    random_source = (random.uniform(0, field_size), random.uniform(0, field_size))

    # Plot the random source
    # ax.plot(random_source[0], random_source[1], marker='o', color='red', markersize=12)
    # ax.text(random_source[0], random_source[1]+20, 'KITT', color='red', fontsize=12, ha='center')

    # Set grid lines and labels
    ax.set_xticks([i for i in range(0, field_size+1, grid_spacing)])
    ax.set_yticks([i for i in range(0, field_size+1, grid_spacing)])
    ax.set_xticks([i for i in range(0, field_size+1, axis_spacing)], minor=False)
    ax.set_yticks([i for i in range(0, field_size+1, axis_spacing)], minor=False)
    ax.grid(True, linestyle='--', linewidth=0.5, which='both')
    ax.grid(True, linestyle='-', linewidth=1, which='major')

    #add label axis
    ax.set_xlabel("y")
    ax.set_ylabel("x")
    ax.yaxis.set_label_position('right')

    # Move the y-axis to the right side
    ax.yaxis.tick_right()

    # Plot black crosses on the specified coordinates
    coordinates = [(400, 80), (160, 305), (240, 240), (120, 240), (320, 140)]
    for coord in coordinates:
        ax.plot(coord[0], coord[1], marker='x', color='black', markersize=8)

    # # Load the visuals if arguments are provided
    # if starting_x is not None and starting_y is not None and orientation is not None and end_x is not None and end_y is not None:
    #     # Plot red cross at end location
    #     ax.plot(end_x, end_y, marker='x', color='red', markersize=12, markeredgewidth=2)
    #
    #     # Add the green arrow annotation
    #     arrow_length = 40
    #     arrow_tail_length = 15
    #     arrow_tail_width = 5
    #     arrow_head_width = 12
    #     arrow_head_length = 12
    #
    #     arrow_dx = arrow_length * np.sin(np.deg2rad(orientation))
    #     arrow_dy = arrow_length * np.cos(np.deg2rad(orientation))
    #
    #     arrow_tail_dx = arrow_tail_length * np.sin(np.deg2rad(orientation))
    #     arrow_tail_dy = arrow_tail_length * np.cos(np.deg2rad(orientation))
    #
    #     arrow_x = starting_x - arrow_tail_dx
    #     arrow_y = starting_y - arrow_tail_dy
    #
    #     ax.annotate('', xy=(arrow_x, arrow_y), xytext=(arrow_x + arrow_dx, arrow_y + arrow_dy),
    #                 arrowprops=dict(arrowstyle='->', linewidth=2, color='green',
    #                                 shrinkA=0, shrinkB=0,
    #                                 connectionstyle=f"arc3,rad={arrow_head_width / arrow_length}",
    #                                 headwidth=arrow_head_width, headlength=arrow_head_length))
    #
    # if waypoint_x is not None and waypoint_y is not None:
    #     # Plot purple star at waypoint location
    #     ax.plot(waypoint_x, waypoint_y, marker='*', color='purple', markersize=12)

        # # Load the RC car image
        # car_image = mpimg.imread('rc-car.ico')
        #
        # # Set the position and orientation of the car image
        # car_width = 30
        # car_height = 20
        # car_position = (starting_x - car_width / 2, starting_y - car_height / 2)
        # car_transform = plt.transforms.Affine2D().rotate_deg(orientation).translate(*car_position)
        #
        # # Plot the car image
        # ax.imshow(car_image, extent=[0, field_size, 0, field_size], transform=car_transform)

    # # Display the plot
    # plt.show()

    # Save the figure as a PNG image
    # fig.savefig('grid_plot.svg')
    return fig



