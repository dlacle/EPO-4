import numpy as np
import matplotlib.pyplot as plt

# File path
file_path = r"C:\Users\ZA\Desktop\EPO-4\EPO-4-Python\Mic-Data\data_mics_kitt_10cm.txt"

# Load data from the text file
data = np.loadtxt(file_path)

# Sampling frequency
fs = 48000

# Total duration
t_total = 10

# Number of peaks
num_peaks = 16

# Calculate the number of samples per peak
samples_per_peak = int(fs * t_total / num_peaks)

# Calculate time vector for a single peak
t = np.linspace(0, t_total/num_peaks, samples_per_peak)

# Reshape data into a 2D array with 16 rows (one for each peak)
data_reshaped = data[:samples_per_peak * num_peaks].reshape((num_peaks, samples_per_peak))

# Calculate the average of all peaks to cancel the noise
average_peak = np.mean(data_reshaped, axis=0)

# Plot the reference signal (amplitude vs time) for the average peak
plt.plot(t, average_peak)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Reference Signal: Amplitude vs Time (Averaged Peak)")
plt.show()