import time
import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from Localization import mic_positions

# Reference signal
ref_sigtest = np.loadtxt(r"C:\Users\Sam\PycharmProjects\EPO-4\Mic-Data\mics_car_2250_bit3k_refclean_threshold950.txt")
ref_sig = ref_sigtest[0:len(ref_sigtest):5]
# Field locations
# data_80x400 = np.loadtxt('Mic-Data/data_mics_kitt_mic_80x400.txt')

data_140x320 = np.loadtxt(r"C:\Users\Sam\PycharmProjects\EPO-4\Mic-Data\data_mics_kitt_carrier_2250_bit_3k_140x320.txt")
data_140x320_0 = data_140x320[0:len(data_140x320):5]


# h = ref_sig
# y_80x400 = np.convolve(x_80x400, h)
# h_80x400 = ch3(x_80x400, y_80x400, Lhat, eps)


def ch3(x, y, Lhat, eps):
    lenx = x.size  # Length of x
    leny = y.size  # Length of y

    l = leny - lenx + 1  # Length of h

    # Force x to be the same length as y
    x = np.append(x, [0] * (l - 1))

    # # Make x the same length as y
    # x = np.concatenate((x, np.zeros(leny - lenx)), axis=None)

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
    # Reference and measured channels
    ch_ref = ch3(x, x, x.size, 0.001)
    ch_measured = ch3(x, y, x.size, 0.001)

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

print(TDOA(ref_sig, data_140x320_0, 48000))

def localization(data1,data2,data3,data4,data5):

    # estimate the channels
    h1 = ch3(x, data1, x.size, 0.001)
    h2 = ch3(x, data2, x.size, 0.001)
    h3 = ch3(x, data3, x.size, 0.001)
    h4 = ch3(x, data4, x.size, 0.001)
    h5 = ch3(x, data5, x.size, 0.001)

    #find the location of the peaks
    location_peak = find_peaks(h1, h2, h3, h4, h5)

    #calculate the difference of the peak locations
    diff_peaks = difference_peaks(location_peak)

    #calculate the cooridanates of the car using the difference of peaks
    estimated_location_KITT = difference_to_location(diff_peaks, mic_positions)
    x = estimated_location_KITT[0]
    y = estimated_location_KITT[1]
    return x, y
def find_peaks(h1, h2, h3, h4, h5):
    peak_ch1 = np.argmax(h1)
    peak_ch2 = np.argmax(h2)
    peak_ch3 = np.argmax(h3)
    peak_ch4 = np.argmax(h4)
    peak_ch5 = np.argmax(h5)

    peak = np.array(peak_ch1, peak_ch2, peak_ch3, peak_ch4, peak_ch5)

    return peak
def difference_peaks(location_peak):
    # Calculate the differences between each pair of elements
    diff_peak = []
    for i in range(len(location_peak)):
        for j in range(i + 1, len(location_peak)):
            diff = abs(location_peak[i] - location_peak[j])
            differences.append(diff)
    return diff_peak


def difference_to_location(diff_peak, mic_positions, Fs):
    Vsound = 343.14 #speed of sound m/s 20 degree
    diff_to_distance = diff_peak*Vsound/Fs

    for i, mic_position in enumerate(mic_positions):
        locals()[f'x{i + 1}'] = mic_position

    # test Print the variables
    for i in range(1, len(mic_positions) + 1):
        print(f'x{i} = {locals()["x" + str(i)]}')

    #define r_ij (Range difference)
    r12 = diff_to_distance[0]
    r13 = diff_to_distance[1]
    r14 = diff_to_distance[2]
    r15 = diff_to_distance[3]
    r23 = diff_to_distance[4]
    r24 = diff_to_distance[5]
    r25 = diff_to_distance[6]
    r34 = diff_to_distance[7]
    r35 = diff_to_distance[8]
    r45 = diff_to_distance[9]

    #define matrix A
    A =np.array([
        [2*(x2-x1),-2*r12,0     ,0     ,0     ],
        [2*(x3-x1),0     ,-2*r13,0     ,0     ],
        [2*(x4-x1),0     ,0     ,-2*r14,0     ],
        [2*(x5-x1),0     ,0     ,0     ,-2*r15],
        [2*(x3-x2),0     ,-2*r23,0     ,0     ],
        [2*(x4-x2),0     ,0     ,-2*r24,0     ],
        [2*(x5-x2),0     ,0     ,0     ,-2*r25],
        [2*(x4-x3),0     ,0     ,-2*r34,0     ],
        [2*(x5-x3),0     ,0     ,0     ,-2*r35],
        [2*(x5-x4),0     ,0     ,0     ,-2*r35]
    ])

    # magnitude / length
    l1 = np.linalg.norm(x1, axis=1)
    l2 = np.linalg.norm(x2, axis=1)
    l3 = np.linalg.norm(x3, axis=1)
    l4 = np.linalg.norm(x4, axis=1)
    l5 = np.linalg.norm(x5, axis=1)

    #define matrix B
    B = np.array([
        [r12**2-l1**2+l2**2],
        [r13**2-l1**2+l3**2],
        [r14**2-l1**2+l4**2],
        [r15**2-l1**2+l5**2],
        [r23**2-l2**2+l3**2],
        [r24**2-l2**2+l4**2],
        [r25**2-l2**2+l5**2],
        [r34**2-l3**2+l4**2],
        [r35**2-l3**2+l5**2],
        [r45**2-l4**2+l5**2]
    ])

    # A*y=B solving for y:
    y = np.linalg.pinv(A)*B

    return y[1], y[2]

# def Average_location(x,y,n_locations = 1):






