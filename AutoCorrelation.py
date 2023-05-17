import numpy as np
import matplotlib.pyplot as plt


def hex_to_binary_array(hex_string):
    # Convert hex string to binary string
    binary_string = bin(int(hex_string, 16))[2:].zfill(32)

    # Convert binary string to NumPy array
    binary_array = np.array(list(binary_string), dtype=int)

    return binary_array



# Define the input sequence
x = hex_to_binary_array("0x3355A780")

# Compute the autocorrelation using numpy.correlate
corr = np.correlate(x, x, mode='full')

# Plot the autocorrelation
plt.stem(corr)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation of Sequence')
plt.show()

print(hex_to_binary_array("0x3355A780"))
