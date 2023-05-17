import numpy as np
import matplotlib.pyplot as plt

# Define the Gold code sequence
hex_num = "3355A780"
bin_num = bin(int(hex_num, 16))[2:]  # Convert hex to int, then to binary
seq = np.array([int(x) for x in bin_num])

# Compute the autocorrelation using numpy's correlate function
autocorr = np.correlate(seq, seq,mode="full")

# Time lag vector for autocorrelation
t_autocorr = np.linspace(-len(autocorr)/2, len(autocorr)/2, len(autocorr))

# Plot the autocorrelation
plt.figure(figsize=(11,4))
plt.stem(t_autocorr,autocorr)
plt.xlabel('Shift')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation of Gold code 3355A780')
plt.show()

