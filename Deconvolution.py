import time
import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

# Define the positions of the 5 microphones x,y,z
mic_positions = np.array(
    [
        [0  ,480, 50],   # mic 1 (bottom left corner)
        [480,480, 50],   # mic 2 (top left corner)
        [480,0  , 50],   # mic 3 (top right corner)
        [0  ,0  , 50],   # mic 4 (bottom right corner)
        [0  ,240, 80]    # mic 5 (side)
    ]
)
Fs = 48000
# File path plot
filename_plot = 'plot_kitt_carrier_2250_bit_3k_80x400_2sec'

# File path mic data
file_path_mic = r"Mic-Data/kitt_carrier_2250_bit_3k_80x400.txt"

# Load data from the text file
data_recording = np.loadtxt(file_path_mic)

# File path ref signal
file_path_xref = r"ref_sig.txt"

# Load data from the text file
xref = np.loadtxt(file_path_xref)

#set eps ch3 function
eps = 0.001

#set speed of sound
Vsound = 343.14 #speed of sound m/s 20 degree


def split_channels(dataTotal):
    N_total = len(dataTotal)
    dataTotal = dataTotal[:len(dataTotal)//5] #only use when u find the recording to long,example for plotting
    data1 = dataTotal[0:N_total:5]
    data2 = dataTotal[1:N_total:5]
    data3 = dataTotal[2:N_total:5]
    data4 = dataTotal[3:N_total:5]
    data5 = dataTotal[4:N_total:5]
    lst = [data1, data2, data3, data4, data5]
    return lst

def find_peak_begin(data):
    total_peak_begin = []
    for i, data_array in enumerate(data):
        # print("Results for data", i + 1)
        # print(len(data_array))
        y_norm = data_array/max(abs(data_array))
        peaks_begin = []
        total_peak_begin.append(peaks_begin)


        counter = 0
        for index,item in enumerate(y_norm):
            if counter >= 0:
                counter -= 1
                continue
            if item > 0.50: #75% of maximum
                peaks_begin.append(index)
                counter = 18000 #after lengt one peak+rest period looking for another peak 8000-22000
        # peaks_begin_debug = [peak / Fs for peak in peaks_begin]
        # print("Peaks Begin:", peaks_begin_debug)
    # peaks_begin_debug = [peak / Fs for peak in peaks_begin]
    # print(total_peak_begin)
    return total_peak_begin #returning a list inside a list [peaks_data1_begin....peaks_data5_begin]


def filterpeaks(total_peak_begin):
    # peaks = [[17787, 37819, 57788, 77820], [106,18270, 38229, 58271, 78224], [18483, 38451, 58633, 78494],
    #      [104, 18188, 38177, 58189, 78178], [17879, 37868, 57881, 77869]]

    # filers out lonely initial peaks
    while True:
        # Get the lowest value of the first element in the sublists
        lowest_value = min(sublist[0] for sublist in total_peak_begin)

        lower_limit = lowest_value - 3000
        upper_limit = lowest_value + 3000

        # Check if all first values are within the interval
        within_interval = all(lower_limit <= sublist[0] <= upper_limit for sublist in total_peak_begin)

        if not within_interval:
            # Remove the lowest overall element from the list
            for sublist in total_peak_begin:
                if sublist[0] == lowest_value:
                    sublist.remove(lowest_value)
        else:
            break

    # filers out lonely final peaks
    while True:
        # Get the highest value of the last element in the sublists
        highest_value = max(sublist[-1] for sublist in total_peak_begin)

        lower_limit = highest_value - 3000
        upper_limit = highest_value + 3000

        # Check if all first values are within the interval
        within_interval = all(lower_limit <= sublist[-1] <= upper_limit for sublist in total_peak_begin)

        if not within_interval:
            # Remove the highest overall element from the list
            for sublist in total_peak_begin:
                if sublist[-1] == highest_value:
                    sublist.remove(highest_value)
        else:
            break
    peak_filter = total_peak_begin
    return peak_filter #returning a list inside a list with filterd [peaks_data1_begin....peaks_data5_begin]

def automatically_segment(peak_filter,lst):
    segments = []
    for p in range(len(peak_filter[0])):
        i = min(sublist[p] for sublist in peak_filter)
        segment_data1 = lst[0][i - 100:i + 12000]
        segment_data2 = lst[1][i - 100:i + 12000]
        segment_data3 = lst[2][i - 100:i + 12000]
        segment_data4 = lst[3][i - 100:i + 12000]
        segment_data5 = lst[4][i - 100:i + 12000]
        segments.extend([segment_data1, segment_data2, segment_data3, segment_data4, segment_data5])

    # segments will contain the desired output
    return segments #returs a list: [segment1_data1..segment1_data5,.....,segment5_data1,..,segment5_data5]

def ch3(x, y, eps):
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
    # # h = h[0:Lhat]
    return h

def find_peaks(h1, h2, h3, h4, h5):
    peak_ch1 = np.argmax(h1)
    peak_ch2 = np.argmax(h2)
    peak_ch3 = np.argmax(h3)
    peak_ch4 = np.argmax(h4)
    peak_ch5 = np.argmax(h5)

    peak_location = np.array([peak_ch1, peak_ch2, peak_ch3, peak_ch4, peak_ch5])

    return peak_location
def difference_peaks(location_peak):
    # Calculate the differences between each pair of elements
    diff_peak = []
    for i in range(len(location_peak)):
        for j in range(i + 1, len(location_peak)):
            diff = abs(location_peak[i] - location_peak[j])
            diff_peak.append(diff)
    return diff_peak #returns a list: [r12,r13,r14,r15,r23,r24,r25,r34,r35,r45]

def difference_to_location(diff_peak, mic_positions, Fs,Vsound):
    diff_to_distance = [x * Vsound for x in diff_peak]
    diff_to_distance = [x /Fs for x in diff_to_distance]

    # for i, mic_position in enumerate(mic_positions):
    #     locals()[f'x{i + 1}'] = mic_position
    #
    # # test Print the variables
    # for i in range(1, len(mic_positions) + 1):
    #     print(f'x{i} = {locals()["x" + str(i)]}')

    # TDOA measurements
    rij = np.array(diff_to_distance)
    xi = mic_positions

    # Constructing the coefficient matrix A
    A = np.zeros((10, 5))
    for i in range(4):
        A[i, :3] = 2 * (xi[i + 1] - xi[0])
        A[i, 3] = -2 * rij[i]

    for i in range(3):
        A[i + 4, :3] = 2 * (xi[i + 2] - xi[i + 1])
        A[i + 4, 3] = -2 * rij[i + 4]

    for i in range(2):
        A[i + 7, :3] = 2 * (xi[i + 3] - xi[i + 1])
        A[i + 7, 3] = -2 * rij[i + 7]

    A[9, :3] = 2 * (xi[4] - xi[3])
    A[9, 4] = -2 * rij[9]

    # Constructing the known vector b
    b = np.zeros(10)
    for i in range(4):
        b[i] = np.linalg.norm(xi[0]) ** 2 - np.linalg.norm(xi[i + 1]) ** 2 + rij[i] ** 2

    for i in range(3):
        b[i + 4] = np.linalg.norm(xi[i + 1]) ** 2 - np.linalg.norm(xi[i + 2]) ** 2 + rij[i + 4] ** 2

    for i in range(2):
        b[i + 7] = np.linalg.norm(xi[i + 1]) ** 2 - np.linalg.norm(xi[i + 3]) ** 2 + rij[i + 7] ** 2

    b[9] = np.linalg.norm(xi[3]) ** 2 - np.linalg.norm(xi[4]) ** 2 + rij[9] ** 2

    # Computing the pseudo-inverse of A
    A_pseudo_inv = np.linalg.pinv(A)

    # Solving for the unknown vector y
    y = np.dot(A_pseudo_inv, b)

    # Extracting the car's location x and nuisance parameters d2, d3, d4, d5
    location = y[:3]
    # d2, d3, d4, d5 = y[3:]

    # Printing the results
    # print("Car Location (x, y, z):", x)
    # print("Nuisance Parameters (d2, d3, d4, d5):", d2, d3, d4, d5)

    #Algorith neglect height

    # x1, x2, x3, x4, x5 = mic_positions
    # #define r_ij (Range difference)
    # r12 = diff_to_distance[0]
    # r13 = diff_to_distance[1]
    # r14 = diff_to_distance[2]
    # r15 = diff_to_distance[3]
    # r23 = diff_to_distance[4]
    # r24 = diff_to_distance[5]
    # r25 = diff_to_distance[6]
    # r34 = diff_to_distance[7]
    # r35 = diff_to_distance[8]
    # r45 = diff_to_distance[9]
    #
    # #define matrix A
    # A = np.array([
    #     [2*(x2-x1),-2*r12,0     ,0     ,0     ],
    #     [2*(x3-x1),0     ,-2*r13,0     ,0     ],
    #     [2*(x4-x1),0     ,0     ,-2*r14,0     ],
    #     [2*(x5-x1),0     ,0     ,0     ,-2*r15],
    #     [2*(x3-x2),0     ,-2*r23,0     ,0     ],
    #     [2*(x4-x2),0     ,0     ,-2*r24,0     ],
    #     [2*(x5-x2),0     ,0     ,0     ,-2*r25],
    #     [2*(x4-x3),0     ,0     ,-2*r34,0     ],
    #     [2*(x5-x3),0     ,0     ,0     ,-2*r35],
    #     [2*(x5-x4),0     ,0     ,0     ,-2*r35]
    # ])
    #
    # # magnitude / length
    # l1 = np.linalg.norm(x1, axis=1)
    # l2 = np.linalg.norm(x2, axis=1)
    # l3 = np.linalg.norm(x3, axis=1)
    # l4 = np.linalg.norm(x4, axis=1)
    # l5 = np.linalg.norm(x5, axis=1)
    #
    # #define matrix B
    # B = np.array([
    #     [r12**2-l1**2+l2**2],
    #     [r13**2-l1**2+l3**2],
    #     [r14**2-l1**2+l4**2],
    #     [r15**2-l1**2+l5**2],
    #     [r23**2-l2**2+l3**2],
    #     [r24**2-l2**2+l4**2],
    #     [r25**2-l2**2+l5**2],
    #     [r34**2-l3**2+l4**2],
    #     [r35**2-l3**2+l5**2],
    #     [r45**2-l4**2+l5**2]
    # ])
    #
    # # A*y=B solving for y:
    # y = np.linalg.pinv(A)*B

    return location

# def Average_location(x,y,n_locations = 1):

def localization(data_recording,x_ref, mic_positions,Fs,eps,Vsound):

    data_per_channel = split_channels(data_recording)

    peak_begin = find_peak_begin(data_per_channel)
    # print('peak begin=',peak_begin)

    filtered_peaks = filterpeaks(peak_begin)
    # print('filtered peak=', filtered_peaks)

    segments = automatically_segment(filtered_peaks, data_per_channel)


    location = []
    for n in range(len(segments)//5): # N segments/peaks, 5 = Nmics

        # estimate the channels
        h1 = ch3(x_ref, segments[n * 5],     eps)
        h2 = ch3(x_ref, segments[n * 5 + 1], eps)
        h3 = ch3(x_ref, segments[n * 5 + 2], eps)
        h4 = ch3(x_ref, segments[n * 5 + 3], eps)
        h5 = ch3(x_ref, segments[n * 5 + 4], eps)

        #find the location of the peaks
        location_peak = find_peaks(h1, h2, h3, h4, h5)

        #calculate the difference of the peak locations
        diff_peaks = difference_peaks(location_peak)

        #calculate the cooridanates of the car using the difference of peaks
        estimated_location_KITT = difference_to_location(diff_peaks, mic_positions,Fs,Vsound)

        location.append(estimated_location_KITT)
    # x = estimated_location_KITT[0]
    # y = estimated_location_KITT[1]
    return location

# # Find_peak_begin(data=lst)
# #
# Plot_each_channel(data1, data2, data3, data4, data5, Fs)
def Plot_each_channel(lst,Fs):

    time = np.linspace(0, len(data1)/Fs, len(data1))

    # Create subplots for each microphone channel
    fig, axs = plt.subplots(5, 1, figsize=(8, 10))

    # Plot the data for each microphone
    axs[0].plot(time, data1, label='Microphone 1')
    axs[1].plot(time, data2, label='Microphone 2')
    axs[2].plot(time, data3, label='Microphone 3')
    axs[3].plot(time, data4, label='Microphone 4')
    axs[4].plot(time, data5, label='Microphone 5')

    # Set labels and title for each subplot
    for i in range(5):
        axs[i].set_ylabel('Amplitude')
        axs[i].set_title('Microphone ' + str(i+1))

    # Set labels and title for the entire figure
    # fig.suptitle('Data of the five microphones', ha='center')
    axs[-1].set_xlabel('Time [s]')

    # Adjust spacing between subplots
    plt.tight_layout()

    # # Export plot
    # plt.savefig(f'Plots-Report/{filename}.svg', format='svg')
    # Display the plot
    plt.show()

    # Plotting 140x320
    data1 = data1/max(data1)
    data4 = data4 / max(data4)
    Fs = 48000
    time_axis = np.linspace(0, len(data1) / Fs, len(data1))
    plt.plot(time_axis, data1, label='mic 1')
    plt.plot(time_axis, data4, label='mic 4')
    plt.legend()

    # Display the plot
    plt.show()
    return

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
print(localization(data_recording,xref,mic_positions,Fs,eps,Vsound))

def Plot_each_channel_in_one_plot(lst, Fs):
    time = np.linspace(0, len(lst[0])/Fs, len(lst[0]))

    # Plot the data for each microphone
    plt.plot(time, lst[0], label='Microphone 1')
    plt.plot(time, lst[1], label='Microphone 2')
    plt.plot(time, lst[2], label='Microphone 3')
    plt.plot(time, lst[3], label='Microphone 4')
    plt.plot(time, lst[4], label='Microphone 5')

    # Set labels and title
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Signals of the five microphones')

    # Add legend
    plt.legend()

    # Display the plot
    plt.show()