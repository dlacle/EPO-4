import numpy as np
import matplotlib.pyplot as plt

# Define the input sequence
x = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0])

# Compute the autocorrelation using numpy.correlate
corr = np.correlate(x, x, mode='full')

# Plot the autocorrelation
plt.stem(corr)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation of Sequence')
plt.show()
