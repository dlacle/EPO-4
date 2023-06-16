import numpy as np
import matplotlib.pyplot as plt

# File path
file_path = r'/epo4/Module2/Module2_mic_array/Mic-Data-V2/kitt_mic3_ref_v2.txt'

# Load data from the text file
data = np.loadtxt(file_path)

#only need data ch 3
ref_ch_3 = data[2:len(data):5]

# Sampling frequency
Fs = 48e3

# Number of samples: 2.4e6
n_samples = len(ref_ch_3)

# Total duration: 50 sec
t_total = n_samples / Fs
t = np.linspace(0, t_total,n_samples)
# #plot everything reference signal
# plt.plot(t,ref_ch_3)
#
# # Calculate auto-correlation
# # autocorr = np.correlate(ref_ch_3, ref_ch_3, mode='full')
# # t_total_autocorr = np.linspace(-t_total/2, t_total/2, len(autocorr))
# # plt.plot(t_total_autocorr,autocorr)
# plt.show()

start_time = 2.4125
end_time = 2.429
start_index = int(start_time * Fs)
end_index = int(end_time * Fs)

clean_data = np.array(ref_ch_3[start_index:end_index])
lenght_clean_data=len(clean_data)

clean_data_nozero = clean_data[clean_data != 0]
lenght_clean_data_nozero =len(clean_data_nozero)

with open('../Mic-Data-V2/ref_sig_V2.1.txt', 'w') as f:
    for i in clean_data_nozero:
        f.write("%s\n" % i)

# Calculate auto-correlation clean_data
autocorr_clean = np.correlate(clean_data, clean_data, mode='full')
#
# Time lag vector for auto-correlation clean_data
t_clean = len(clean_data) / Fs
t_autocorr_clean = np.linspace(-t_clean/2, t_clean/2, len(autocorr_clean))
#
# Calculate auto-correlation clean_data_nozero
autocorr_clean_nozero = np.correlate(clean_data_nozero, clean_data_nozero, mode='full')
#
# Time lag vector for auto-correlation clean_data_nozero
t_clean_nozero = lenght_clean_data_nozero / Fs
tt_clean_nozero =np.linspace(0, t_clean_nozero ,lenght_clean_data_nozero)
t_autocorr_clean_nozero = np.linspace(-t_clean_nozero/2, t_clean_nozero/2, len(autocorr_clean_nozero))

# Create subplots with 2 rows and 2 columns
fig, axs = plt.subplots(2, 2)

# Plot the reference signal for one peak
axs[0, 0].plot(t[start_index:end_index], clean_data)
axs[0, 0].set_xlabel("Time [s]")
axs[0, 0].set_ylabel("Amplitude")
axs[0, 0].set_title("Reference Signal one peak")

# Plot the auto-correlation of reference signal for one peak
axs[0, 1].plot(t_autocorr_clean, autocorr_clean)
axs[0, 1].set_xlabel("Time Lag [s]")
axs[0, 1].set_ylabel("Amplitude")
axs[0, 1].set_title("Auto-correlation of one peak reference Signal")
#
# Plot cleaned reference signal
axs[1, 0].plot(tt_clean_nozero, clean_data_nozero)
axs[1, 0].set_xlabel("Time [s]")
axs[1, 0].set_ylabel("Amplitude")
axs[1, 0].set_title("Reference Signal: Cleaned")

# Plot the auto-correlation of cleaned signal
axs[1, 1].plot(t_autocorr_clean_nozero, autocorr_clean_nozero )
axs[1, 1].set_xlabel("Time Lag [s]")
axs[1, 1].set_ylabel("Amplitude")
axs[1, 1].set_title("Auto-correlation of Cleaned Reference Signal")

plt.tight_layout()
plt.show()