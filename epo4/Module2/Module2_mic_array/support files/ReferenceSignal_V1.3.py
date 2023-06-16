import numpy as np
import matplotlib.pyplot as plt

# File path
file_path = r'../Mic-Data/Mic-Data-V1/ref_ch3_V1.txt'

# Load data from the text file
data = np.loadtxt(file_path)

# Sampling frequency
Fs = 48e3

# Number of samples: 2.4e6
n_samples = len(data)

# Total duration: 50 sec
t_total = n_samples / Fs
# start_time = 5.146
# end_time = 5.17
start_time = 3.475
end_time = 3.51
start_index = int(start_time * Fs)
end_index = int(end_time * Fs)

clean_data = np.array(data[start_index:end_index])

clean_data = clean_data[clean_data != 0]
# lenght_clean_data_nozero =len(clean_data)
with open('../Mic-Data/Mic-Data-V1/ref_sig_V1.8.txt', 'w') as f:
    for i in clean_data:
        f.write("%s\n" % i)

# Calculate auto-correlation
autocorr_clean = np.correlate(clean_data, clean_data, mode='full')

# Time lag vector for auto-correlation
t_total_clean = len(clean_data) / Fs
t_clean= np.linspace(start_time,end_time,len(clean_data))
t_autocorr_clean = np.linspace(-t_total_clean/2, t_total_clean/2, len(autocorr_clean))

# Create subplots with 2 rows and 2 columns
fig, axs = plt.subplots(2, 1)

# Plot cleaned reference signal
axs[0].plot(t_clean, clean_data)
axs[0].set_xlabel("Time [s]")
axs[0].set_ylabel("Amplitude")
axs[0].set_title("Reference Signal: Cleaned")

# Plot the auto-correlation of cleaned signal
axs[1].plot(t_autocorr_clean, autocorr_clean)
axs[1].set_xlabel("Time Lag [s]")
axs[1].set_ylabel("Amplitude")
axs[1].set_title("Auto-correlation of Cleaned Reference Signal")

plt.tight_layout()
plt.show()