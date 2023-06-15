import math
import time
import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy import stats
from scipy.linalg import norm
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Define Constants and variables
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Define the positions of the 5 microphones x,y,z (in cm)
mic_positions_xyz = np.array(
    [
        [0  ,480, 50],   # mic 1 (bottom left corner)
        [480,480, 50],   # mic 2 (top left corner)
        [480,0  , 50],   # mic 3 (top right corner)
        [0  ,0  , 50],   # mic 4 (bottom right corner)
        [0  ,240, 80]    # mic 5 (side)
    ]
)

mic_positions_xy = np.array(
    [
        [0  ,480],   # mic 1 (bottom left corner)
        [480,480],   # mic 2 (top left corner)
        [480,0  ],   # mic 3 (top right corner)
        [0  ,0  ],   # mic 4 (bottom right corner)
        [0  ,240]    # mic 5 (side)
    ]
)
Fs = 48000

# File path mic data
file_path_mic = r"C:\Users\Sam\PycharmProjects\EPO-4\epo4\Module2\Module2_mic_array\Mic-Data-V2\kitt_mic_80x400_v2.txt"
location_car = '140x240'
location_car = [80,400]

# Load data from the text file
data_recording = np.loadtxt(file_path_mic)

# File path ref signal
file_path_xref = r"C:\Users\Sam\PycharmProjects\EPO-4\epo4\Module2\Module2_mic_array\Mic-Data-V2\ref_sig_V2.1.txt"

# Load data from the text file
xref = np.loadtxt(file_path_xref)
print('lenght xref=',len(xref))

#set eps ch3 function
eps = 0.001

#set speed of sound
Vsound = 343.14 #speed of sound m/s 20 degree

#set treshold for find first peak channel response
threshold = 0.27 #0.25

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Plotting functions:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def Plot_each_channel_separately(lst, Fs,location_car):
    time = np.linspace(0, len(lst[0]) / Fs, len(lst[0]))

    # Create subplots for each microphone channel
    fig, axs = plt.subplots(5, 1, figsize=(8, 10))

    # Plot the data for each microphone
    axs[0].plot(time, lst[0], label='Microphone 1')
    axs[1].plot(time, lst[1], label='Microphone 2')
    axs[2].plot(time, lst[2], label='Microphone 3')
    axs[3].plot(time, lst[3], label='Microphone 4')
    axs[4].plot(time, lst[4], label='Microphone 5')

    # Set labels and title for each subplot
    for i in range(5):
        axs[i].set_ylabel('Amplitude')
        axs[i].set_title('Microphone ' + str(i + 1))

    # Set labels and title for the entire figure
    # fig.suptitle('Data of the five microphones', ha='center')
    axs[-1].set_xlabel('Time [s]')

    # Adjust spacing between subplots
    plt.tight_layout()

    #main title
    fig.suptitle(f'Recording of each channel at location {location_car}')

    # Adjust spacing between subplots
    plt.subplots_adjust(top=0.9, hspace=0.5)

    # Export plot
    # plt.savefig('Signals of each channels at 400x400.svg', format='svg')
    # Display the plot
    plt.show()
    return

def Plot_each_channel_in_one_plot_color(lst, Fs, location_car):
    time = np.linspace(0, len(lst[0]) / Fs, len(lst[0]))

    # Define colors and alpha values for each microphone
    colors = ['red', 'green', 'blue', 'orange', 'purple']
    alpha_values = [1.0, 0.8, 0.6, 0.4, 0.2]

    # Plot the data for each microphone with different colors and transparency
    for i in range(len(lst)):
        plt.plot(time, lst[i], label=f'Microphone {i + 1}', color=colors[i], alpha=alpha_values[i])

    # Set labels and title
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title(f'Recording of the 5 channels at {location_car}')

    # Add legend
    plt.legend()

    # Display the plot
    # plt.savefig('Signals of the 5 channels at 80x400 diff color.svg', format='svg')
    plt.show()
    return
def Plot_each_channel_in_one_plot(lst, Fs, location_car):
    time = np.linspace(0, len(lst[0]) / Fs, len(lst[0]))

    # Plot the data for each microphone
    plt.plot(time, lst[0], label='Microphone 1')
    plt.plot(time, lst[1], label='Microphone 2')
    plt.plot(time, lst[2], label='Microphone 3')
    plt.plot(time, lst[3], label='Microphone 4')
    plt.plot(time, lst[4], label='Microphone 5')

    # Set labels and title
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title(f'Signals of the five microphones {location_car}')

    # Add legend
    plt.legend()

    # Display the plot
    plt.show()
    return

def Plot_each_segment_and_each_channel_separately(segment, Fs, location_car,n,lowest_peak_value):
    time = np.linspace((lowest_peak_value[n] -950) / Fs, (lowest_peak_value[n]-950) / Fs + len(segment[n*5]) / Fs, len(segment[n*5]))

    fig, axs = plt.subplots(5, 1, figsize=(8, 10))

    # Plot the data for each microphone with different colors and transparency
    axs[0].plot(time, segment[n*5], label='mic 1')
    axs[1].plot(time, segment[n*5+1], label='mic 2')
    axs[2].plot(time, segment[n*5+2], label='mic 3')
    axs[3].plot(time, segment[n*5+3], label='mic 4')
    axs[4].plot(time, segment[n*5+4], label='mic 5')

    # Set labels and title for each subplot
    for i, ax in enumerate(axs):
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'Channel {i + 1}')
        ax.legend()

    # Add a vertical line to each subplot
    for ax in axs:
        ax.axvline(x=lowest_peak_value[n]/Fs, color='r', linestyle='--')

    # Adjust spacing between subplots
    plt.subplots_adjust(top=0.9, hspace=0.65)
    # plt.subplots_adjust(top=0.9, hspace=0.1)  # Increased hspace value for more room

    #main titel
    fig.suptitle(f'Each channel of Segment {n + 1} at location {location_car}')

    # Save the plot
    # plt.savefig('Channel_response_of_3e_segment_at_location_140x320.svg', format='svg')

    # Display the plot
    plt.show()
    return


def Plot_all_channels_per_segment_one_plot(segment, Fs, location_car, n, lowest_peak_value):
    time = np.linspace((lowest_peak_value[n]-950) / Fs, (lowest_peak_value[n]-950 )/ Fs + len(segment[n*5]) / Fs, len(segment[n*5])+500)

    # Define colors and alpha values for each microphone
    colors = ['red', 'green', 'blue', 'orange', 'purple']
    alpha_values = [1.0, 0.8, 0.6, 0.4, 0.2]

    # Plot the data for each microphone with different colors and transparency
    plt.plot(time, segment[n*5], label=f'Microphone 1', color='red', alpha=0.7)
    plt.plot(time, segment[n*5+1], label=f'Microphone 2', color='green', alpha=0.7)
    plt.plot(time, segment[n*5+2], label=f'Microphone 3', color='blue', alpha=0.6)
    plt.plot(time, segment[n*5+3], label=f'Microphone 4', color='orange', alpha=0.4)
    plt.plot(time, segment[n*5+4], label=f'Microphone 5', color='purple', alpha=0.2)

    # # Add a dot or line at time = lowest_peak_value[n]/Fs
    # plt.scatter(lowest_peak_value[n] / Fs,0, color='black', marker='o', s=30)
    plt.axvline(x=lowest_peak_value[n]/Fs, color='r', linestyle='--')

    # Set labels and title
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title(f'Channel response of {n+1}e segment at location {location_car}')

    # Add legend
    plt.legend()

    # Display the plot
    # plt.savefig('Channel_response_of_3e_segment_at_location_140x3200_color.svg', format='svg')
    plt.show()

    return


def plotting_channel_response_of_every_chanel_of_every_segment(n, lowest_peak_value, h1, h2, h3, h4, h5):
    # plotting the channel response of every chanel of every segment
    time = np.linspace((lowest_peak_value[n] - 1000) / Fs, (lowest_peak_value[n] + len(h1)) / Fs, len(h1)+1000)

    # Create subplots for each microphone channel
    fig, axs = plt.subplots(5, 1, figsize=(8, 10))

    # Plot the data for each microphone
    axs[0].plot(time, h1, label='Microphone 1')
    axs[1].plot(time, h2, label='Microphone 2')
    axs[2].plot(time, h3, label='Microphone 3')
    axs[3].plot(time, h4, label='Microphone 4')
    axs[4].plot(time, h5, label='Microphone 5')

    # Set labels and title for each subplot
    for i in range(5):
        axs[i].set_ylabel('Amplitude')
        axs[i].set_xlabel('Time [s]')
        axs[i].set_title('Channel ' + str(i + 1))

    # Set labels and title for the entire figure
    # fig.suptitle('Data of the five microphones', ha='center')
    axs[-1].set_xlabel('Time [s]')

    # Adjust spacing between subplots
    plt.tight_layout()

    fig.suptitle(f'Channel inpulse response of each channel for segment {n + 1} at location {location_car}')

    # Adjust spacing between subplots
    plt.subplots_adjust(top=0.9, hspace=0.5)

    # Export plot
    # plt.savefig('Signals of each channels at 400x400.svg', format='svg')
    # Display the plot
    plt.show()
    return

def plotting_channel_response_of_every_channel_in_one_plot_each_segment(n, lowest_peak_value, h1, h2, h3, h4, h5, peak_location):
    # Define the colors for each channel
    colors = ['limegreen', 'lightblue', 'red', 'purple', 'orange']
    alpha_values = [0.8, 0.7, 0.6, 0.4, 0.2]

    # Calculate the time axis
    #time = np.linspace((lowest_peak_value[n] - 100) / Fs, (lowest_peak_value[n] + len(h1)) / Fs, len(h1))


    # Create a single plot for all microphone channels
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the data for each microphone with colors corresponding to peak locations
    for i, (h, peak) in enumerate(zip([h1, h2, h3, h4, h5], peak_location)):
        time = np.linspace(0, len(h), len(h))
        ax.plot(time, h, label=f'Microphone {i + 1}', color=colors[i],alpha = alpha_values[i])
        ax.axvline(x=peak / Fs, color=colors[i], linestyle='--')

    # Set labels and title
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')
    ax.set_title(f'Channel Impulse Response of Each Channel for Segment {n + 1} at Location {location_car}')
    ax.legend()

    # Display the plot
    plt.show()
    return


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def split_channels(dataTotal):
    N_total = len(dataTotal)
    dataTotal = dataTotal[:N_total//1] #only use when u find the recording to long,example for plotting
    data1 = dataTotal[0:len(dataTotal):5]
    data2 = dataTotal[1:len(dataTotal):5]
    data3 = dataTotal[2:len(dataTotal):5]
    data4 = dataTotal[3:len(dataTotal):5]
    data5 = dataTotal[4:len(dataTotal):5]
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
            if item > 0.50: #50% of maximum
                peaks_begin.append(index)
                counter = 18000 #after lengt one peak+rest period looking for another peak 8000-22000
        # peaks_begin_debug = [peak / Fs for peak in peaks_begin]
        # print("Peaks Begin:", peaks_begin_debug)
    # peaks_begin_debug = [peak / Fs for peak in peaks_begin]
    print('peaks_begin=',total_peak_begin)
    return total_peak_begin #returning a list inside a list [[peaks_data1_begin]....[peaks_data5_begin]]


def filterpeaks(total_peak_begin):

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
    print('peaks_begin_filtered=',peak_filter)
    return peak_filter #returning a list inside a list with filtered [peaks_data1_begin....peaks_data5_begin]

def automatically_segment(peak_filter,lst):
    segments = []

    for p in range(len(peak_filter[0])):
        i = min(sublist[p] for sublist in peak_filter)
        segment_data1 = lst[0][i - 950:i + 15000]
        segment_data2 = lst[1][i - 950:i + 15000]
        segment_data3 = lst[2][i - 950:i + 15000]
        segment_data4 = lst[3][i - 950:i + 15000]
        segment_data5 = lst[4][i - 950:i + 15000]
        segments.extend([segment_data1, segment_data2, segment_data3, segment_data4, segment_data5])

    #only use for debug and plotting
    which_channel_first = []
    lowest_peak_value = []
    for p in range(len(peak_filter[0])):
        lowest_peak = min(sublist[p] for sublist in peak_filter)
        sublist_index = next(i for i, sublist in enumerate(peak_filter) if sublist[p] == lowest_peak)
        print(f"lowest peak of each segment = {lowest_peak}, {lowest_peak/Fs}sec, came from sublist [{sublist_index}]")
        which_channel_first.append(sublist_index)
        lowest_peak_value.append(lowest_peak)

    # segments will contain the desired output
    return segments, which_channel_first, lowest_peak_value #returs a list: [segment1_data1..segment1_data5,.....,segment5_data1,..,segment5_data5] , which_channel first gives which channel has the lowest value on given segment, lowest_peak_value gives the value of that segment


def ch3(x, y, eps,Lhat):
    """
    Channel estimation using deconvolution in frequency domain
       :param x: Reference signal
       :param y: Measured signal
       :param lhat: Length
       :param epsi: Threshold ignore values below this to reduce noise amplification
       :return: Estimated channel
    """
    lenx = x.size  # Length of x
    leny = y.size  # Length of y

    l = leny - lenx + 1  # Length of h

# if sbd
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
def find_peaks(h1, h2, h3, h4, h5,treshold):
    peak_ch1 = find_first_pk(h1,treshold)
    peak_ch2 = find_first_pk(h2,treshold)
    peak_ch3 = find_first_pk(h3,treshold)
    peak_ch4 = find_first_pk(h4,treshold)
    peak_ch5 = find_first_pk(h5,treshold)

    peak_location = np.array([peak_ch1, peak_ch2, peak_ch3, peak_ch4, peak_ch5])
    print(peak_location)

    return peak_location
def difference_peaks(location_peak):
    # Calculate the differences between each pair of elements
    diff = np.empty([4, 4])
    for i in range(4):
        for j in range(4):
            diff[i, j] = (location_peak[i] - location_peak[j])
    print(diff)
    return diff #returns a matrix: [[r11,r12,r13,r14],[r21,r22,r23,r24],[r31,r32,r33,r34],[r41,r42,r43,r44]]

def difference_to_location_xyz(diff_peak, mic_positions_xyz, Fs,Vsound):
    """
    Locate KITT using the time difference of arrival of a sound signal
    :param mic_positions_xyz: (Nx5) array containing recordings from all 5 microphones
    :param ref: reference recording
    :param Fs: sample frequency
    :param test: if test is given [x, y, z] uses get_distances to generate a perfect distmat
    :return: coordinates of KITT [x, y, z]
    """

    # Multiply each element of diff by Vsound / Fs to get difference in distance (cm) instead of frames
    diff_peak = diff_peak * (Vsound / Fs *100)

    print(diff_peak)

    # If a coordinate is parsed in the test argument, get_distances will be used to generate the
    # TDOA distance matrix, to test the localisation algorithm, otherwise a TDOA matrix will be
    # generated from the micarray, using the channel-estimation and TDOA functions.

    # Localisation algorithm
    b = np.zeros(6)
    A = np.zeros([6, 5])
    k = 0
    for i in range(4):
        for j in range(i + 1, 4):
            A[k, 0] = 2 * (mic_positions_xyz[j, 0] - mic_positions_xyz[i, 0])
            A[k, 1] = 2 * (mic_positions_xyz[j, 1] - mic_positions_xyz[i, 1])
            # A[k, 2] = 2 * (mic_positions_xyz[j, 2] - mic_positions_xyz[i, 2]).T
            A[k, j + 1] = - 2 * diff_peak[i, j]
            k += 1

    k = 0
    for i in range(4):
        for j in range(i + 1, 4):
            b[k] = (diff_peak[i, j] ** 2 - norm(mic_positions_xyz[i]) ** 2 + norm(mic_positions_xyz[j]) ** 2)
            k += 1

    A[A == 0] = 1e-12
    location = np.matmul(np.linalg.pinv(A), b)[:2]
    if diff_peak[1, 1] != 0:
        location - [10, 10]

    return location
def localization(data_recording,x_ref, mic_positions,Fs,eps,Vsound,Lhat, location_car,treshold):

    data_per_channel = split_channels(data_recording)

    # Plot_each_channel_in_one_plot_color(data_per_channel, Fs, location_car)
    # Plot_each_channel_separately(data_per_channel, Fs, location_car)

    peak_begin = find_peak_begin(data_per_channel)
    # print('peak begin=',peak_begin)

    filtered_peaks = filterpeaks(peak_begin)
    # print('filtered peak=', filtered_peaks)

    segments, which_channel_first, lowest_peak_value = automatically_segment(filtered_peaks, data_per_channel)
    location = []
    # channel = []
    for n in range(len(segments)//5): # N segments/peaks, 5 = Nmics/channels

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                Only use when you have a low number of peaks
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        # Plot_each_segment_and_each_channel_separately(segments, Fs, location_car, n, lowest_peak_value)
        # Plot_all_channels_per_segment_one_plot(segments, Fs, location_car, n, lowest_peak_value)
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        # estimate the channels
        h1 = ch3(x_ref, segments[n * 5],     eps,Lhat)
        h2 = ch3(x_ref, segments[n * 5 + 1], eps,Lhat)
        h3 = ch3(x_ref, segments[n * 5 + 2], eps,Lhat)
        h4 = ch3(x_ref, segments[n * 5 + 3], eps,Lhat)
        h5 = ch3(x_ref, segments[n * 5 + 4], eps,Lhat)
        # channel.extend([h1,h2,h3,h4,h5])

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Only use when you have a low number of peaks
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        # plotting_channel_response_of_every_chanel_of_every_segment(n,lowest_peak_value,h1,h2,h3,h4,h5)
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


        #find the location of the peaks
        location_peak = find_peaks(h1, h2, h3, h4, h5,treshold)
        # plotting_channel_response_of_every_channel_in_one_plot_each_segment(n, lowest_peak_value, h1, h2, h3, h4, h5, location_peak)


        #calculate the difference of the peak locations
        diff_peaks = difference_peaks(location_peak)

        #calculate the cooridanates of the car using the difference of peaks
        # estimated_location_KITT = difference_to_location_xy(diff_peaks, mic_positions,Fs,Vsound)
        estimated_location_KITT = difference_to_location_xyz(diff_peaks, mic_positions, Fs, Vsound)

        location.append(estimated_location_KITT)
    # x = estimated_location_KITT[0]
    # y = estimated_location_KITT[1]

    # Plot_each_channel_in_one_plot(data_per_channel, Fs, location_car)
    # Plot_one_segment_each_channel_in_one_plot (channel, Fs, location_car)
    # Plot_one_segment_each_channel(channel, Fs, location_car)

    # Convert locations to normal array format
    location = [[loc[0], loc[1]] for loc in location]

    # print(location)

    return location
def IQR_average(locations):
    locations_array = np.array(locations)

    x_iqr = stats.iqr(locations_array[:, 0])
    y_iqr = stats.iqr(locations_array[:, 1])

    x_lower_bound = np.percentile(locations_array[:, 0], 25) - (1.5 * x_iqr)
    x_upper_bound = np.percentile(locations_array[:, 0], 75) + (1.5 * x_iqr)

    y_lower_bound = np.percentile(locations_array[:, 1], 25) - (1.5 * y_iqr)
    y_upper_bound = np.percentile(locations_array[:, 1], 75) + (1.5 * y_iqr)

    filtered_locations = locations_array[(locations_array[:, 0] >= x_lower_bound) &
                                         (locations_array[:, 0] <= x_upper_bound) &
                                         (locations_array[:, 1] >= y_lower_bound) &
                                         (locations_array[:, 1] <= y_upper_bound)]

    average_location_within_iqr = np.mean(filtered_locations, axis=0)

    print("Average location (x, y) within IQR range:", average_location_within_iqr)

    return average_location_within_iqr

locations = localization(data_recording, xref, mic_positions_xy, Fs, eps, Vsound, len(xref), location_car, threshold)
print(locations)
location = IQR_average(locations)
print(location)

# Calculate the distance using the Euclidean distance formula
error = abs(math.sqrt((location[0] - location_car[0]) ** 2 + (location[1] - location_car[1]) ** 2))
print(error)




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




def TDOA(x, y, Fs):
    # Reference and measured channels
    h_3 = ch3(x, data3, x.size, 0.001)
    h_1 = ch3(x, data1, x.size, 0.001)

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


# # Plotting 140x320
    # data1 = data1/max(data1)
    # data4 = data4 / max(data4)
    # Fs = 48000
    # time_axis = np.linspace(0, len(data1) / Fs, len(data1))
    # plt.plot(time_axis, data1, label='mic 1')
    # plt.plot(time_axis, data4, label='mic 4')
    # plt.legend()