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
    t_start = 2  # Start time (seconds)
    t_end = 2.25  # End time (seconds)

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


def find_first_pk(data, threshold):
    # Normalize the data to [0, 1]
    normalized_data = data / max(abs(data))

    # Find the indices where the data crosses the threshold
    above_threshold_indices = np.where(normalized_data > threshold)[0]

    if len(above_threshold_indices) == 0:
        return None  # No peak above the threshold

    # Find the first peak index
    first_peak_index = above_threshold_indices[0]

    return first_peak_index


def TDOA(x, y, Fs):
    # Start and end time
    t_start = 2.00
    t_end = 2.25

    # Indices corresponding to the desired time range
    start_index = int(t_start * Fs)
    end_index = int(t_end * Fs)

    # First and second channels
    y_ch_first = y[0:len(y):5][start_index:end_index]
    y_ch_second = y[2:len(y):5][start_index:end_index]

    # Response of first and second channels
    h_first = ch3(x, y_ch_first, 0.001, x.size)
    h_second = ch3(x, y_ch_second, 0.001, x.size)

    # The time axis for the impulse response is
    # then created using the length of the first
    # channel and the sampling rate
    t = np.linspace(0, len(h_first) / Fs, len(h_first))

    # Find the peak of each of the impulse responses
    # above a certain threshold
    pk_h_first_thresh = find_first_pk(h_first, 0.25)
    pk_h_second_thresh = find_first_pk(h_second, 0.25)

    # Print first peak locations
    print(f'Location of first peak h1: {pk_h_first_thresh}')
    print(f'Location of first peak h2: {pk_h_second_thresh}\n')

    # Create subplots for each microphone channel
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))

    # Add a title to the figure
    fig.suptitle('Channel impulse responses')

    # Plot implulse responses
    axs[0].plot(h_first)
    axs[1].plot(h_second)

    # Add titles to each subplot
    axs[0].set_title('First channel')
    axs[1].set_title('Second channel')

    # Set common labels
    fig.supxlabel('')
    fig.supylabel('Amplitude')

    # Include grid
    axs[0].grid()
    axs[1].grid()

    # Add red dots at the first peaks
    axs[0].scatter(pk_h_first_thresh, h_first[pk_h_first_thresh], color="red")
    axs[1].scatter(pk_h_second_thresh, h_second[pk_h_second_thresh], color="red")

    plt.show()

    # Time difference between two peaks (in samples)
    t_diff = t[pk_h_second_thresh] - t[pk_h_first_thresh]

    # Distance between two signals is obtained by
    # multiplying the time difference by speed of sound
    distance = 343 * t_diff

    return distance


def main():

    # Sampling frequency
    Fs = 48e3

    # Mics positions (x, y, z)
    mic_positions = [
        [0, 480, 50],  # Microphone 1
        [480, 480, 50],  # Microphone 2
        [480, 0, 50],  # Microphone 3
        [0, 0, 50],  # Microphone 4
        [0, 240, 80]  # Microphone 5
    ]

    # Reference signal
    x = np.loadtxt('ref_sig_V1.8.txt')

    # Beacon signal location
    y = np.loadtxt('Mic-Data/kitt_carrier_2250_bit_3k_80x400.txt')

    # Compute TDOA
    distance = TDOA(x, y, Fs)
    print(f'Distance {distance} [meter]')

    # plotting(x, y, Fs)


if __name__ == '__main__':
    main()
