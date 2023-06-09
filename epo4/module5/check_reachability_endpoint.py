import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arrow

def check_endpoint_reachability(startx, starty, init_orientation, driving_radius, endx, endy):
    # Calculate the center of the circles
    centerx1 = startx + driving_radius * math.cos(math.radians(init_orientation - 90))
    centery1 = starty + driving_radius * math.sin(math.radians(init_orientation - 90))

    centerx2 = startx + driving_radius * math.cos(math.radians(init_orientation + 90))
    centery2 = starty + driving_radius * math.sin(math.radians(init_orientation + 90))

    # Calculate the distance between the endpoint and the centers of the circles
    distance1 = math.sqrt((endx - centerx1) ** 2 + (endy - centery1) ** 2)
    distance2 = math.sqrt((endx - centerx2) ** 2 + (endy - centery2) ** 2)

    # Check if the distances are greater than or equal to the driving radius for both circles
    if distance1 >= driving_radius and distance2 >= driving_radius:
        return True

    return False

def plot_check_endpoint_reachability(startx, starty, init_orientation, driving_radius, endx, endy, save_path=None):
    # Calculate the center of the circles
    centerx1 = startx + driving_radius * math.cos(math.radians(init_orientation - 90))
    centery1 = starty + driving_radius * math.sin(math.radians(init_orientation - 90))

    centerx2 = startx + driving_radius * math.cos(math.radians(init_orientation + 90))
    centery2 = starty + driving_radius * math.sin(math.radians(init_orientation + 90))

    # Check if the endpoint is valid
    valid = check_endpoint_reachability(startx, starty, init_orientation, driving_radius, endx, endy)

    # Plotting
    fig, ax = plt.subplots()

    # Plot the circles
    circle1 = Circle((centerx1, centery1), driving_radius, edgecolor='b', facecolor='None', linestyle='--')
    circle2 = Circle((centerx2, centery2), driving_radius, edgecolor='r', facecolor='None', linestyle='--')
    ax.add_artist(circle1)
    ax.add_artist(circle2)

    # Plot the start point
    ax.plot(startx, starty, 'go', label='Start Point')

    # Plot the endpoint
    if valid:
        ax.plot(endx, endy, 'ro', label='Endpoint (Valid)')
    else:
        ax.plot(endx, endy, 'ro', label='Endpoint (Invalid)')

    # Plot the orientation arrow and add it to the legend
    orientation_arrow = Arrow(startx, starty, driving_radius * math.cos(math.radians(init_orientation)),
                              driving_radius * math.sin(math.radians(init_orientation)),
                              color='m', width=0.5)
    ax.add_artist(orientation_arrow)

    # Set axis limits and labels
    ax.set_xlim(startx - driving_radius - 5, startx + driving_radius + 5)
    ax.set_ylim(starty - driving_radius - 5, starty + driving_radius + 5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_aspect('equal')

    # Include all the items in the legend
    handles, labels = ax.get_legend_handles_labels()
    handles.append(circle1)
    labels.append('Circle 1')
    handles.append(circle2)
    labels.append('Circle 2')
    handles.append(orientation_arrow)
    labels.append('KITT Arrow')
    ax.legend(handles, labels, loc='upper left', fontsize='small')

    plt.title('Endpoint Validity Plot')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot as a PNG file if save_path is provided
    if save_path:
        plt.savefig(save_path, format='svg')

    plt.show()
    return

# Example usage
startx = 0
starty = 0
init_orientation = 90
driving_radius = 5
endx = 2.5
endy = 2.5

save_path = ""  #module5_plots_rapport/check_endpoint_reachability_valid2.svg
plot_check_endpoint_reachability(startx, starty, init_orientation, driving_radius, endx, endy, save_path=save_path)

print(check_endpoint_reachability(startx, starty, init_orientation, driving_radius, endx, endy))
