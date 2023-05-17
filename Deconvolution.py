import time
import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

# Reference signal
ref_sig = np.loadtxt('Mic-Data/data_mics_kitt_carrier_2250_bit_3k_ref.txt')

# Field locations
data_80x400 = np.loadtxt('Mic-Data/data_mics_kitt_mic_80x400.txt')
data_140x320 = np.loadtxt('Mic-Data/data_mics_kitt_mic_140x320.txt')

h = ref_sig
y_80x400 = np.convolve(x_80x400, h)
h_80x400 = ch3(x_80x400, y_80x400, Lhat, eps)


def ch3(x, y, Lhat, eps):
    lenx = x.size  # Length of x
    leny = y.size  # Length of y

    # Make x the same length as y
    x = np.concatenate((x, np.zeros(leny - lenx)), axis=None)

    # Deconvolution in frequency domain
    Y = fft(y)
    X = fft(x)

    # Obtain frequency response
    H = Y / X

    H[np.absolute(X) < eps * max(np.absolute(X))] = 0

    # Compute time-domain impulse response, make result real
    h = np.real(ifft(H))

    return h


def TDOA(x, y, Fs):
    # Reference and measured channels
    ch_ref = ch3(x, x, x.size, 0.01)
    ch_measured = ch3(x, y, x.size, 0.01)

    # The time axis for the impulse response is
    # then created using the length of the reference
    # channel and the sampling rate.
    t = np.linspace(0, len(ch_ref)/Fs, len(ch_ref))

    # Find the peak of each of the impulse responses
    # using the argmax() function. This assumes that
    # the peak represents the arrival
    # time of the direct sound between the two signals.
    pk_ref = np.argmax(ch_ref)
    pk_measured = np.argmax(ch_measured)

    # Time difference between two peaks (in samples)
    t_diff = t[pk_measured] - t[pk_ref]

    # Distance between two signals is obtained by
    # multiplying the time difference by speed of sound
    distance = 343 * t_diff

    return distance
