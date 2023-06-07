import numpy as np
import matplotlib.pyplot as plt

# Some example data
x = np.linspace(0, 10, 200)
y = np.sin(x)

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the data
ax.plot(x, y)

# Set the x-axis tick marks at 0.5 intervals
ax.set_xticks(np.arange(0, 10.5, 0.5))

# Show the plot
plt.show()
