import numpy as np
import matplotlib.pyplot as plt

# Define the Gold code sequence
hex_num = "3355A780"
bin_num = bin(int(hex_num, 16))[2:]  # Convert hex to int, then to binary
print(len(bin_num))
seq = np.array([int(x) for x in bin_num])
print(seq)
# Compute the autocorrelation using numpy's correlate function
autocorr = np.correlate(seq, seq,mode="full")

# nr = (range(0,(2*len(seq)-1)))


# Plot
plt.figure(figsize=(11,4))
plt.stem(autocorr)

# Plot the autocorrelation
plt.xlabel('Shift')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation of Gold code 3355A780')
plt.show()

