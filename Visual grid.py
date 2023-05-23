import matplotlib.pyplot as plt
import random

def visuel_grid():
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
    ax.plot(random_source[0], random_source[1], marker='o', color='red', markersize=12)
    ax.text(random_source[0], random_source[1]+20, 'KITT', color='red', fontsize=12, ha='center')

    # Set grid lines and labels
    ax.set_xticks([i for i in range(0, field_size+1, grid_spacing)])
    ax.set_yticks([i for i in range(0, field_size+1, grid_spacing)])
    ax.set_xticks([i for i in range(0, field_size+1, axis_spacing)], minor=False)
    ax.set_yticks([i for i in range(0, field_size+1, axis_spacing)], minor=False)
    ax.grid(True, linestyle='--', linewidth=0.5, which='both')
    ax.grid(True, linestyle='-', linewidth=1, which='major')

    # Move the y-axis to the right side
    ax.yaxis.tick_right()

    # # Display the plot
    # plt.show()

