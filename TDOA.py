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

    G = [i if abs(i) > eps else 0 for i in X]

    # Compute time-domain impulse response, make result real
    Hhat = np.multiply(H, G)
    h = ifft(Hhat)
    # h = h[0:Lhat]
    return np.real(abs(h))


def TDOA(x, y, Fs):

    t_start = 2  # Start time (seconds)
    t_end = 2.25  # End time (seconds)

    # Find the indices corresponding to the desired time range
    start_index = int(t_start * Fs)
    end_index = int(t_end * Fs)

    y_ch1 = y[0:len(y):5][start_index:end_index]
    y_ch3 = y[2:len(y):5][start_index:end_index]

    # Reference and measured channels
    h_1 = ch3(x, y_ch1, 0.001, x.size)
    h_3 = ch3(x, y_ch3, 0.001, x.size)

    # The time axis for the impulse response is
    # then created using the length of the reference
    # channel and the sampling rate.
    t = np.linspace(0, len(h_1) / Fs, len(h_1))
    # Create subplots for each microphone channel
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))

    axs[0].plot(h_1, label='Microphone 1')
    axs[1].plot(h_3, label='Microphone 3')

    # Adjust spacing between subplots
    plt.tight_layout()
    # axs.grid

    # Plot the data
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(f'Channel estimation recording 240x240')


    # Find the peak of each of the impulse responses
    # using the argmax() function. This assumes that
    # the peak represents the arrival
    # time of the direct sound between the two signals.
    pk_h1 = np.argmax(h_1)
    pk_h3 = np.argmax(h_3)
    print(pk_h1, pk_h3)
    axs[0].scatter(pk_h1, h_1[pk_h1], color="red")
    axs[1].scatter(pk_h3, h_3[pk_h3], color="red")
    plt.show()
    # Time difference between two peaks (in samples)
    t_diff = t[pk_h3] - t[pk_h1]

    # Distance between two signals is obtained by
    # multiplying the time difference by speed of sound
    distance = 343 * t_diff

    return distance


def main():

    Fs = 48e3
    x = np.loadtxt('ref_sig_V1.8.txt')
    y = np.loadtxt('Mic-Data/kitt_carrier_2250_bit_3k_240x240.txt')

    distance = TDOA(x, y, Fs)
    print("Distance:", distance, ' [meter]')

    plotting(x, y, Fs)

if __name__ == '__main__':
    main()
