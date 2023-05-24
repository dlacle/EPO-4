import numpy as np
import matplotlib.pyplot as plt

# File path
file_path = r'Mic-Data/kitt_carrier_2250_bit_3k_ref.txt'

# Load data from the text file
data = np.loadtxt(file_path)

# Sampling frequency
Fs = 48000

# Number of samples: 2.4e6
n_samples = len(data)

# Total duration: 50 sec
t_total = n_samples / Fs

# Number of peaks
num_peaks = 12

# Calculate the number of samples per peak
samples_per_peak = int(n_samples / num_peaks)

# Calculate time vector for a single peak
t = np.linspace(0, t_total / num_peaks, samples_per_peak)

# Reshape data into a 2D array with 16 rows (one for each peak)
data_reshaped = data[:samples_per_peak * num_peaks].reshape((num_peaks, samples_per_peak))

# Calculate the average of all peaks to cancel the noise
average_peak = np.mean(data_reshaped, axis=0)

# Calculate auto-correlation
autocorr = np.correlate(average_peak, average_peak, mode='full')
t_autocorr = np.linspace(-t_total, t_total, len(autocorr))

# # Calculate auto-correlation
# autocorr = np.correlate(average_peak, average_peak, mode='full')
#
# # Time lag vector for auto-correlation
# t_autocorr = np.linspace(-t_total, t_total, len(autocorr))
#
# # Clean up the recording by removing zero intervals
# # clean_data = average_peak[np.nonzero(average_peak)]
#
# threshold = 950  # Adjust this value according to your needs
#
# # Find the indices where the peak values exceed the threshold
# peak_indices = np.where(abs(average_peak) > threshold)[0]
#
# # Find the start and end indices of the non-zero interval
# # start_index = peak_indices[0]
# # end_index = peak_indices[-1]

# Trim the average peak to remove the zero intervals

start_time = 0.75
end_time = 1.3
start_index = int(start_time * 48000)
end_index = int(end_time * 48000)

clean_data = average_peak[start_index:end_index]

# Calculate auto-correlation
autocorr_clean = np.correlate(clean_data, clean_data, mode='full')

# Time lag vector for auto-correlation
t_total_clean = len(clean_data) / Fs
t_autocorr_clean = np.linspace(-t_total_clean/2, t_total_clean/2-1, len(clean_data))

# Plot the reference signal for the averaged peaks
plt.subplot(221)
plt.plot(t, average_peak)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Reference Signal: Averaged Peaks")

# Plot the auto-correlation of reference signal
plt.subplot(222)
plt.plot(t_autocorr, autocorr)
plt.xlabel("Time Lag (s)")
plt.ylabel("Auto correlation")
plt.title("Auto-correlation of Reference Signal")

# Plot cleaned reference signal
plt.subplot(223)
plt.plot(t[start_index:end_index], clean_data)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Reference Signal: Cleaned")

# Plot the auto-correlation of cleaned signal
plt.subplot(224)
plt.plot(t_autocorr_clean, autocorr_clean)
plt.xlabel("Time Lag (s)")
plt.ylabel("Auto-correlation")
plt.title("Auto-correlation of Cleaned Reference Signal")

plt.tight_layout()
plt.show()
