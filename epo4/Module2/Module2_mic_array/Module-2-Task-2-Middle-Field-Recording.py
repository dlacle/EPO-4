import numpy as np
import matplotlib.pyplot as plt

fs = int(48e3)
signal = np.loadtxt('Mic-Data/kitt_middle.txt')

# Reshape the interleaved data into separate channels
num_channels = 5
channel_data = np.reshape(signal, (-1, num_channels))

# Calculate time axis
num_samples = channel_data.shape[0]
time = np.arange(num_samples) / fs

# Define the start and end times for the plot
start_time = 0.39  # seconds
end_time = 0.5  # seconds

# Find the corresponding indices in the time array
start_index = int(start_time * fs)
end_index = int(end_time * fs)

# Create subplots for each microphone channel
fig, axs = plt.subplots(num_channels, 1, figsize=(8, 10))

# Plot the data of all five channels
for i in range(num_channels):
    axs[i].plot(time[start_index:end_index], channel_data[start_index:end_index, i])
    axs[i].set_ylabel('Amplitude')
    axs[i].set_title(f'Microphone {i + 1}')
    axs[i].set_ylim(-500, 500)  # Set y-axis limits

# Set x-axis label for the last subplot
axs[-1].set_xlabel('Time [s]')

# Adjust spacing between subplots
plt.tight_layout()

# Export plot
plt.savefig('Plots-Final-Report/Task2-middle-v2.svg', format='svg')

# Display the plot
plt.show()
