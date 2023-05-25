import numpy as np
import matplotlib.pyplot as plt

# Define the data
data = "00110011010101011010011110000000"

# Define the carrier frequency and period
fc = 2250  # in Hz
Tc = 1 / fc  # in seconds

# Define the sampling frequency and period
fs = 48e3  # in Hz
Ts = 1 / fs  # in seconds

# Create the time vector
t = np.arange(0, len(data) * Tc, Ts)

# Generate the OOK waveform
ook = np.zeros(len(t))
for i in range(len(data)):
    if data[i] == "1":
        ook[i * int(Tc / Ts):(i + 1) * int(Tc / Ts)] = 1

# Plot the OOK waveform
plt.plot(t, ook)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Ideal OOK waveform (gold code: 0x3355A780)')
plt.savefig('Plots-Report/IdealOOK.svg', format='svg')
plt.show()
