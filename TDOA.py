import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

def plotting(x, y, Fs):

    y_ch1 = y[0:len(y):5]
    y_ch2 = y[1:len(y):5]
    y_ch3 = y[2:len(y):5]
    y_ch4 = y[3:len(y):5]
    y_ch5 = y[4:len(y):5]

    # Calculate the time axis
    t = np.arange(len(y_ch3)) / Fs

    # Set the time range for the plot
    t_start =2  # Start time (seconds)
    t_end =  2.25 # End time (seconds)

    # Find the indices corresponding to the desired time range
    start_index = int(t_start * Fs)
    end_index = int(t_end * Fs)

    # Create subplots for each microphone channel
    fig, axs = plt.subplots(6, 1, figsize=(8, 10))

    # Extract the data within the desired time range
    t_range = t[start_index:end_index]

    axs[0].plot(t_range, y_ch1[start_index:end_index], label='Microphone 1')
    axs[1].plot(t_range, y_ch2[start_index:end_index], label='Microphone 2')
    axs[2].plot(t_range, y_ch3[start_index:end_index], label='Microphone 3')
    axs[3].plot(t_range, y_ch4[start_index:end_index], label='Microphone 4')
    axs[4].plot(t_range, y_ch5[start_index:end_index], label='Microphone 5')
    # axs[5].plot(t_range, x[start_index:end_index], label='ref')

    # Adjust spacing between subplots
    plt.tight_layout()
    # axs.grid

    # Plot the data
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(f'KITT recording 240x240')
    plt.show()


def ch3(x, y, eps, Lhat):
    lenx = x.size  # Length of x
    leny = y.size  # Length of y

    l = leny - lenx + 1  # Length of h

    if lenx < leny:
        x = np.concatenate((x, np.zeros(leny - lenx)))
    else:
        y = np.concatenate((y, np.zeros(lenx - leny)))

    # Force x to be the same length as y
    # x = np.append(x, [0] * (l - 1))

    # # Make x the same length as y
    # x = np.concatenate(x, np.zeros(leny - lenx))

    # Deconvolution in frequency domain
    Y = fft(y)
    X = fft(x)

    # Obtain frequency response
    H = Y / X

    H[np.absolute(X) < eps * max(np.absolute(X))] = 0

    # Compute time-domain impulse response, make result real
    h = np.real(ifft(H))
    # h = h[0:Lhat]
    return h


def TDOA(x, y, Fs):

    t_start = 0.35  # Start time (seconds)
    t_end = 0.45  # End time (seconds)

    # Find the indices corresponding to the desired time range
    start_index = int(t_start * Fs)
    end_index = int(t_end * Fs)

    y_ch1 = y[0:len(y):5][start_index:end_index]
    y_ch3 = y[2:len(y):5][start_index:end_index]

    # Reference and measured channels
    ch_ref = ch3(x, y_ch1, 0.002, x.size)
    ch_mesaured = ch3(x, y_ch3, 0.002, x.size)

    # The time axis for the impulse response is
    # then created using the length of the reference
    # channel and the sampling rate.
    t = np.linspace(0, len(ch_ref) / Fs, len(ch_ref))
    # Create subplots for each microphone channel
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))

    axs[0].plot(t, ch_ref, label='Microphone 1')
    axs[1].plot(t, ch_mesaured, label='Microphone 3')

    # Adjust spacing between subplots
    plt.tight_layout()
    # axs.grid

    # Plot the data
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(f'Channel estimation recording 240x240')
    plt.show()

    # Find the peak of each of the impulse responses
    # using the argmax() function. This assumes that
    # the peak represents the arrival
    # time of the direct sound between the two signals.
    pk_ref = np.argmax(ch_ref)
    pk_measured = np.argmax(ch_mesaured)

    # Time difference between two peaks (in samples)
    t_diff = t[pk_measured] - t[pk_ref]

    # Distance between two signals is obtained by
    # multiplying the time difference by speed of sound
    distance = 343 * t_diff

    return distance


def main():

    Fs = 48e3
    x = np.loadtxt('ref_sig_V1.5.txt')
    y = np.loadtxt('Mic-Data/kitt_carrier_2250_bit_3k_240x240.txt')

    distance = TDOA(x, y, Fs)
    print("Distance:", distance, ' [meter]')

    plotting(x, y, Fs)

if __name__ == '__main__':
    main()
