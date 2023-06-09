import numpy as np
import matplotlib.pyplot as plt

# File path
file_path = r'Mic-Data/kitt_carrier_2250_bit_3k_ref.txt'

# Load data from the text file
data = np.loadtxt(file_path)

#exstract data mic 3 out data
N_total = len(data)
data = data[2:N_total:5] #data mic 3

# Sampling frequency
Fs = 48e3

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Plot the reference signal
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
time = np.linspace(0, len(data) / Fs, len(data))

# Plot the data
plt.plot(time, data)

# Set labels and title
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Recording of reference signal')
# plt.savefig('Signals of each channels at 400x400.svg', format='svg')
plt.show()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Average the signal
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''
Compute the num of peaks automatic
'''''''''''''''''''''''''''''''''
# Number of samples: 2.4e6
n_samples = len(data)

# Total duration: 50 sec
t_total = n_samples / Fs

# Number of peaks
y_norm = data/max(abs(data))
peaks_begin = []

counter = 0
for index,item in enumerate(y_norm):
    if counter >= 0:
        counter -= 1
        continue
    if item > 0.80: #80% of maximum
        peaks_begin.append(index)
        counter = 18000 #after lengt one peak+rest period looking for another peak 8000-22000
print('peaks_begin=',peaks_begin)
peak_begin_sec = [peak / Fs for peak in peaks_begin]
print('peaks begin sec =',peak_begin_sec)
print('number of peaks=',len(peaks_begin))

num_peaks = len(peaks_begin)

# # Calculate the number of samples per peak
# samples_per_peak = int(n_samples / num_peaks)
#
# # Calculate time vector for a single peak
# t = np.linspace(0, t_total / num_peaks, samples_per_peak)
#
# # Reshape data into a 2D array with N rows (one for each peak)
# data_reshaped = data[:samples_per_peak * num_peaks].reshape((num_peaks, samples_per_peak))
#
# # Calculate the average of all peaks to cancel the noise
# average_peak = np.mean(data_reshaped, axis=0)

''''''''''''''''''''''''''''''''''
split and average the peaks
'''''''''''''''''''''''''''''''''
# Split the signal into individual pulses
pulses = np.split(data, num_peaks)

# # Calculate the average pulse
# average_pulse = np.mean(pulses, axis=0)
#
# # Subtract the average pulse from each individual pulse to remove noise
# denoised_pulses = [pulse - average_pulse for pulse in pulses]
#
# # Concatenate the denoised pulses back into a single signal
# denoised_signal = np.concatenate(denoised_pulses)

# Calculate the average pulse
average_pulse = np.mean(pulses, axis=0)
t_average_pulse = np.linspace(0,len(average_pulse)/Fs,len(average_pulse))
plt.plot(t_average_pulse,average_pulse)
plt.show()
# Remove noise by subtracting the average pulse from each individual pulse
denoised_pulses = []
for pulse in pulses:
    denoised_pulse = pulse - average_pulse
    denoised_pulses.append(denoised_pulse)

# denoised_pulses now contains the denoised individual pulses
# If you want to combine the denoised pulses back into a single signal
denoised_signal = np.sum(denoised_pulses, axis=0)
''''''''''''''''''''''''''''''''''
plot the  average peak
'''''''''''''''''''''''''''''''''
average_peak = denoised_signal
t = np.linspace(0, len(average_peak) / Fs, len(average_peak))

# Plot the data
plt.plot(t, average_peak)

# Set labels and title
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Recording of denoised/average reference signal')
# plt.savefig('Signals of each channels at 400x400.svg', format='svg')
plt.show()


# Calculate auto-correlation
average_peak = denoised_signal
autocorr = np.correlate(average_peak, average_peak, mode='full')
t_autocorr = np.linspace((-len(autocorr)/Fs)/2, (len(autocorr)/Fs)/2, len(autocorr)) #t_autocorr = np.linspace(-t_total, t_total, len(autocorr))

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Clean the average_peak visualy
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
start_time = 0.145
end_time = 0.175
start_index = int(start_time * Fs)
end_index = int(end_time * Fs)

clean_data = np.array(average_peak[start_index:end_index])
clean_data = clean_data[clean_data != 0]
print(len(clean_data))

#Save the data
with open('ref_sig_V1.2.txt', 'w') as f:
    for i in clean_data:
        f.write("%s\n" % i)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Plot the average ref signal and its autocorrolation
Plot the cleaned ref signal and its autocorrolation
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Calculate auto-correlation
autocorr_clean = np.correlate(clean_data, clean_data, mode='full')

# Time lag vector for auto-correlation
t_autocorr_clean = len(autocorr_clean) / Fs
t_autocorr_clean = np.linspace(-t_autocorr_clean/2, t_autocorr_clean/2, len(autocorr_clean))

# Create subplots with 2 rows and 2 columns
fig, axs = plt.subplots(2, 2,figsize=(10, 10))

# Plot the reference signal for the averaged peaks
axs[0, 0].plot(t, average_peak)
axs[0, 0].set_xlabel("Time [s]")
axs[0, 0].set_ylabel("Amplitude")
axs[0, 0].set_title("Reference Signal: Averaged Peaks")

# Plot the auto-correlation of reference signal
axs[0, 1].plot(t_autocorr, autocorr)
axs[0, 1].set_xlabel("Time Lag [s]")
axs[0, 1].set_ylabel("Amplitude")
axs[0, 1].set_title("Auto-correlation of averaged reference Signal")

# Plot cleaned reference signal
t_clean_data = np.linspace(0,len(clean_data)/Fs,len(clean_data))
axs[1, 0].plot(t_clean_data, clean_data)
axs[1, 0].set_xlabel("Time [s]")
axs[1, 0].set_ylabel("Amplitude")
axs[1, 0].set_title("Reference Signal: Cleaned")

# Plot the auto-correlation of cleaned signal
axs[1, 1].plot(t_autocorr_clean, autocorr_clean)
axs[1, 1].set_xlabel("Time Lag [s]")
axs[1, 1].set_ylabel("Amplitude")
axs[1, 1].set_title("Auto-correlation of Cleaned Reference Signal")

plt.tight_layout()
plt.show()
