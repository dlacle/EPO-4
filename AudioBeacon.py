"""
Audio beacon and code transmission of Module 2
"""

import time
import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Sampling data
Fs = 48000
Time_recording = 10  # in seconds
N_mic = 5  # number of mics/channels
N = Time_recording * Fs  # number of frames per mic
N_total = N_mic * N  # total number of samples


def start_pairing(comport='COM7'):
    """
    This function starts the pairing mode to KITT,
    transmission takes place over port 7
    """

    # global comport

    global serial_port
    serial_port = serial.Serial(comport, 115200, rtscts=True)

    print("connected")

    # Audio beacon command
    # time.sleep(1)
    # On
    serial_port.write(b'A1\n')

    time.sleep(5)
    # Carrier freq = 7 kHz
    carrier_frequency = (7000).to_bytes(2, byteorder='big')
    serial_port.write(b'F' + carrier_frequency + b'\n')
    time.sleep(0.1)

    # Bit freq = 2 kHz
    bit_frequency = (2000).to_bytes(2, byteorder='big')
    serial_port.write(b'B' + bit_frequency + b'\n')
    time.sleep(0.1)

    # Repetition count = bit freq / repetition freq
    repetition_count = (1250).to_bytes(2, byteorder='big')
    serial_port.write(b'R' + repetition_count + b'\n')
    time.sleep(0.1)

    # Gold code
    code = 0x3355A780.to_bytes(4, byteorder='big')
    serial_port.write(b'C' + code + b'\n')
    time.sleep(0.1)


    return


def mic_recording():
    # Create instance of PyAudio
    pyaudio_handle = pyaudio.PyAudio()

    # List the index and names of all audio devices visible to PyAudio
    for i in range(pyaudio_handle.get_device_count()):
        device_info = pyaudio_handle.get_device_info_by_index(i)
        print(i, device_info['name'])

    ####################[Automate the correct PyAudio device index]###############
    desired_device_name = "Microphone (AudioBox 1818 VSL)"
    desired_channels = 1

    for i in range(pyaudio_handle.get_device_count()):
        device_info = pyaudio_handle.get_device_info_by_index(i)
        if (device_info["name"] == desired_device_name):
            device_index = i
            break

    stream = pyaudio_handle.open(input_device_index=device_index,
                                 channels=5,
                                 format=pyaudio.paInt16,
                                 rate=Fs,
                                 input=True)
    ###############################################################################

    # Recording of N frames

    # Recording and storing mic data
    samples = stream.read(N)
    data = np.frombuffer(samples, dtype='int16')
    with open('unnamed.txt', 'w') as file:
        for sample in data:
            file.write("%s\n" % sample)
        print("data stored")
    return


def plotting():
    # Plotting the microphone data
    dataTotal = np.loadtxt('unnamed.txt')

    data0 = dataTotal[0:N_total:5]
    data1 = dataTotal[1:N_total:5]
    data2 = dataTotal[2:N_total:5]
    data3 = dataTotal[3:N_total:5]
    data4 = dataTotal[4:N_total:5]

    # Create an array for time based on the length of the data
    time_total = np.arange(len(dataTotal)) / Fs
    time = np.arange(len(data0)) / Fs

    # Plot Datatotal
    plt.plot(time_total, dataTotal)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Audio Recording')

    # Plot each channel

    # Create subplots for each microphone channel
    fig, axs = plt.subplots(5, 1, figsize=(8, 10))

    # Plot the data for each microphone
    axs[0].plot(time, data0, label='Microphone 0')
    axs[1].plot(time, data1, label='Microphone 1')
    axs[2].plot(time, data2, label='Microphone 2')
    axs[3].plot(time, data3, label='Microphone 3')
    axs[4].plot(time, data4, label='Microphone 4')

    # Set labels and title for each subplot
    for i in range(5):
        axs[i].set_ylabel('Amplitude')
        axs[i].set_title('Microphone ' + str(i))

    # Set labels and title for the entire figure
    # fig.suptitle('Data of the five microphones', ha='center')
    axs[-1].set_xlabel('Time [s]')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Export plot
    plt.savefig('/Plots/unnamed.svg', format='svg')

    # Display the plot
    plt.show()
    return

def stop_pairing():
    serial_port.write(b'A0\n')  # off
    time.sleep(0.1)
    # close connection
    serial_port.close()
    print("disconnected")
    return

def main():
    start_pairing()
    # mic_recording()
    # plotting()
    stop_pairing()
    return

main()