import numpy as np
import matplotlib.pyplot as plt

# File path
file_path_ref = r'../Mic-Data/kitt_carrier_2250_bit_3k_ref.txt'

# Load data from the text file
data = np.loadtxt(file_path_ref)

# Select
ref_ch_3 = data[2:2400000:5][4.5:]

# Sampling frequency
Fs = 48e3

# Number of samples: 2.4e6
n_samples = len(ref_ch_3)

# Total duration: 50 sec
t_total = n_samples / Fs


# Calculate time vector for a single peak
t = np.arange(len(ref_ch_3)) / Fs


# Calculate auto-correlation
autocorr = np.correlate(ref_ch_3, ref_ch_3, mode='full')
t_autocorr = np.arange(-len(ref_ch_3)//2, len(ref_ch_3)//2)

start_time = 0
end_time = 10
start_index = int(start_time * Fs)
end_index = int(end_time * Fs)

# clean_data = np.array(average_peak[start_index:end_index])
# lenght_clean_data=len(clean_data)
# clean_data = clean_data[clean_data != 0]
# lenght_clean_data_nozero =len(clean_data)


# Calculate auto-correlation
# autocorr_clean = np.correlate(clean_data, clean_data, mode='full')

# # Time lag vector for auto-correlation
# t_total_clean = len(clean_data) / Fs
# t_autocorr_clean = np.linspace(-t_total_clean/2, t_total_clean/2, len(autocorr_clean))

# Create subplots with 2 rows and 2 columns
fig, axs = plt.subplots(2, 2)

# Plot the reference signal
axs[0, 0].plot(t, ref_ch_3)
axs[0, 0].set_xlabel("Time [s]")
axs[0, 0].set_ylabel("Amplitude")
axs[0, 0].set_title("Reference Signal")

# # Plot the auto-correlation of reference signal
# axs[0, 1].plot(t_autocorr, autocorr)
# axs[0, 1].set_xlabel("Lag")
# axs[0, 1].set_ylabel("Amplitude")
# axs[0, 1].set_title("Auto-correlation of Reference Signal")

# # Plot cleaned reference signal
# axs[1, 0].plot(t[start_index:end_index - (lenght_clean_data-lenght_clean_data_nozero)], clean_data)
# axs[1, 0].set_xlabel("Time [s]")
# axs[1, 0].set_ylabel("Amplitude")
# axs[1, 0].set_title("Reference Signal: Cleaned")
#
# # Plot the auto-correlation of cleaned signal
# axs[1, 1].plot(t_autocorr_clean, autocorr_clean)
# axs[1, 1].set_xlabel("Time Lag [s]")
# axs[1, 1].set_ylabel("Amplitude")
# axs[1, 1].set_title("Auto-correlation of Cleaned Reference Signal")

# plt.tight_layout()
# plt.savefig(f'Plots-Report/autocorrelation-comparison.svg', format='svg')

plt.show()