import numpy as np
import matplotlib.pyplot as plt

data = '00110011010101011010011110000000'
Fc = 2250  # Hz
Fbit = len(data) * 20  # 32 bits in 1 second
Fs = 48e3

samples_per_bit = int(Fs / Fbit)  # Calculate the number of samples per bit


def analog_ook_waveform(data, Fc, Fbit, samples_per_bit):
    Tbit = 1 / Fbit

    t_analog = np.linspace(0, len(data) * Tbit, len(data) * samples_per_bit, endpoint=False)

    carrier_wave = np.sin(2 * np.pi * Fc * t_analog)

    ook_analog = np.zeros_like(t_analog)
    for i, bit in enumerate(data):
        if bit == '1':
            start_index = int(i * samples_per_bit)
            end_index = int((i + 1) * samples_per_bit)
            ook_analog[start_index:end_index] = carrier_wave[start_index:end_index]

    return t_analog, ook_analog


t_analog, ook_analog = analog_ook_waveform(data, Fc, Fbit, samples_per_bit)


def digital_ook_waveform(data, Fc, sampling_freq):
    Tc = 1 / Fc * 3.5
    Ts = 1 / sampling_freq

    t_digital = np.arange(0, len(data) * Tc, Ts)
    ook_digital = np.zeros(len(t_digital))

    for i in range(len(data)):
        if data[i] == "1":
            start_index = int(i * Tc / Ts)
            end_index = int((i + 1) * Tc / Ts)
            ook_digital[start_index:end_index] = 1

    return t_digital, ook_digital


t_digital, ook_digital = digital_ook_waveform(data, Fc, Fs)

# Create subplots with 2 rows and 1 column
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot analog OOK
axs[0].plot(t_analog, ook_analog)
axs[0].set_title('Ideal analog OOK waveform (gold code: 0x3355A780)')
axs[0].set_xlabel('Time [s]')
axs[0].set_ylabel('Amplitude')
axs[0].grid(True)

# Plot digital OOK
axs[1].plot(t_digital, ook_digital)
axs[1].set_title('Ideal digital OOK waveform (gold code: 0x3355A780)')
axs[1].set_xlabel('Time [s]')
axs[1].set_ylabel('Amplitude')
axs[1].grid(True)

# Adjust spacing between subplots
plt.subplots_adjust(hspace=0.5)
plt.savefig('Plots-Report/IdealOOK-2.svg', format='svg')

# Display the plot
plt.show()
