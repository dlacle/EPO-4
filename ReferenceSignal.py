import numpy as np
import matplotlib.pyplot as plt

# File path
file_path = r"Mic-Data/data_mics_kitt_carrier_2250_bit_3k_ref.txt"

# Load data from the text file
data = np.loadtxt(file_path)

# Sampling frequency
fs = 48000

# Total duration
t_total = len(data)/fs

# Number of peaks
num_peaks = 12

# Calculate the number of samples per peak
samples_per_peak = int(fs * t_total / num_peaks)

# Calculate time vector for a single peak
t = np.linspace(0, t_total/num_peaks, samples_per_peak)

# Reshape data into a 2D array with 16 rows (one for each peak)
data_reshaped = data[:samples_per_peak * num_peaks].reshape((num_peaks, samples_per_peak))

# Calculate the average of all peaks to cancel the noise
average_peak = np.mean(data_reshaped, axis=0)

# Calculate autocorrelation
autocorr = np.correlate(average_peak, average_peak, mode='full')

# Time lag vector for autocorrelation
t_autocorr = np.linspace(-t_total, t_total, len(autocorr))




# Clean up the recording by removing zero intervals
# clean_data = average_peak[np.nonzero(average_peak)]

threshold = 950 # Adjust this value according to your needs

# Find the indices where the peak values exceed the threshold
peak_indices = np.where(abs(average_peak)> threshold)[0]

# Find the start and end indices of the non-zero interval
start_index = peak_indices[0]
end_index = peak_indices[-1]

# Trim the average peak to remove the zero intervals
clean_data = average_peak[start_index:end_index+1]

with open('Mic-Data/data_mics_kitt_carrier_2250_bit3k_ref_clean_nozero.txt', 'w') as file:
    for sample in data:
        file.write("%s\n" % sample)

# Plot the reference signal (amplitude vs time) for the average peak
plt.figure(figsize=(12, 4))
plt.subplot(141)
plt.plot(t, average_peak)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Reference Signal: Amplitude vs Time (Averaged Peak)")

# # Plot the autocorrelation
# plt.subplot(142)
# plt.plot(t_autocorr,autocorr)
# plt.xlabel("Time Lag (s)")
# plt.ylabel("Autocorrelation")
# plt.title("Autocorrelation of Average Peak")
#
# #plot clean data
# plt.subplot(143)
# plt.plot(t[:len(clean_data)], clean_data)
# # plt.plot(t[start_index:end_index+1], clean_peak)
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.title("Clean Single Pulse")
#
# plt.subplot(144)
# t_c = np.linspace(-t_total, t_total, len(clean_data))
# C_c = np.correlate(clean_data, clean_data, mode='full')
# plt.plot(C_c)
# plt.xlabel("Time Lag (s)")
# plt.ylabel("Autocorrelation")
# plt.title("Autocorrelation of Average Peak")

plt.tight_layout()
plt.show()