import numpy as np
import matplotlib.pyplot as plt

time_period = 0.5*1e-2  # seconds
duty_cycle = 0.5  # 50% duty cycle
carrier_freq = 2250  # Hz

# Define time steps
num_samples = 1000  # number of samples
time_step = time_period / num_samples
time = np.arange(0, time_period, time_step)

# Generate OOK signal
signal = np.zeros(num_samples)
on_time = duty_cycle * time_period
num_on_samples = int(on_time / time_step)
signal[:num_on_samples] = 1

# Generate carrier signal
carrier = np.sin(2 * np.pi * carrier_freq * time)

# Modulate carrier with OOK signal
modulated_signal = signal * carrier

# Plot modulated signal
plt.plot(time, modulated_signal)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('OOK Modulated Signal')
plt.show()