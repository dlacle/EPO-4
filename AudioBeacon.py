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
filename = 'data_mics_kitt_carrier_2250_bit_3k_ref'

def start_pairing(comport='COM7'):
    """
    This function starts the pairing mode to KITT,
    transmission takes place over port 7
    """

    # global comport
    global serial_port
    # getting access to bluetooth link
    try:
        serial_port = serial.Serial(comport, 115200, rtscts=True)
        print("Port details ->", serial_port)
    except serial.SerialException as var:
        print("Error has occured")
        print("var")
    else:
        print("connected, serial port opened")

    # Carrier freq = 7 kHz
    carrier_frequency = (3000).to_bytes(2, byteorder='big')
    serial_port.write(b'F' + carrier_frequency + b'\n')
    time.sleep(0.1)

    # Bit freq = 2 kHz
    bit_frequency = (1500).to_bytes(2, byteorder='big')
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

    # On
    serial_port.write(b'A1\n')

    # Speaker playback duration
    time.sleep(2)

    return


def mic_recording():
    # Create instance of PyAudio
    pyaudio_handle = pyaudio.PyAudio()

    # List the index and names of all audio devices visible to PyAudio
    for i in range(pyaudio_handle.get_device_count()):
        device_info = pyaudio_handle.get_device_info_by_index(i)
        print(i, device_info['name'])

    # Automate the correct PyAudio device index
    desired_device_name1 = "Microphone (AudioBox 1818 VSL)"
    desired_device_name2 = "Microphone (2- AudioBox 1818 VS"
    desired_device_name3 = "Microphone (2- AudioBox 1818 VSL)"


    for i in range(pyaudio_handle.get_device_count()):
        device_info = pyaudio_handle.get_device_info_by_index(i)
        if (device_info["name"] == desired_device_name1 or
            device_info["name"] == desired_device_name2 or
            device_info["name"] == desired_device_name3):
            device_index = i
            break

    stream = pyaudio_handle.open(input_device_index=device_index,
                                 channels=5,
                                 format=pyaudio.paInt16,
                                 rate=Fs,
                                 input=True)


    # Recording and storing mic data
    samples = stream.read(N)
    data = np.frombuffer(samples, dtype='int16')
    with open(f'Mic-Data/{filename}.txt', 'w') as file:
        for sample in data:
            file.write("%s\n" % sample)
        print("data stored")
    return


def plotting():
    # Plotting the microphone data
    dataTotal = np.loadtxt(f'Mic-Data/{filename}.txt')

    # data0 = dataTotal[0:N_total:5]
    # data1 = dataTotal[1:N_total:5]
    data2 = dataTotal[2:N_total:5]
    # data3 = dataTotal[3:N_total:5]
    # data4 = dataTotal[4:N_total:5]

    # Create an array for time based on the length of the data
    time_total = np.arange(len(dataTotal)) / Fs
    time = np.arange(len(data2)) / Fs

    # Plot Datatotal
    plt.plot(time, data2)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Audio Recording')

    # Plot each channel

    # Create subplots for each microphone channel
    # fig, axs = plt.subplots(5, 1, figsize=(8, 10))

    # Plot the data for each microphone
    # axs[0].plot(time, data0, label='Microphone 0')
    # axs[1].plot(time, data1, label='Microphone 1')
    plt.plot(time, data2, label='Microphone 2')
    # axs[3].plot(time, data3, label='Microphone 3')
    # axs[4].plot(time, data4, label='Microphone 4')

    # Set labels and title for each subplot
    # for i in range(5):
    #     axs[i].set_ylabel('Amplitude')
    #     axs[i].set_title('Microphone ' + str(i))
    #
    # # Set labels and title for the entire figure
    # # fig.suptitle('Data of the five microphones', ha='center')
    # axs[-1].set_xlabel('Time [s]')
    #
    # # Adjust spacing between subplots
    # plt.tight_layout()

    # Export plot
    plt.savefig(f'Plots/{filename}.svg', format='svg')

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
    mic_recording()
    plotting()
    stop_pairing()
    return

main()


# 1. 11111111111111111111111111111111
# 2. 11001001010110011010101101100000
# 3. 10110010101100110101011011000001
# 4. 01100101011001101010110110000011
# 5. 11001101010011010101101100000110
# 6. 10011010100110101011011000001101
# 7. 00110101001101010110110000011011
# 8. 01101010011010101101100000110110
# 9. 11010100110101011011000001101101
# 10. 10101001101010110110000011011011
# 11. 01010011010101101100000110110110
# 12. 10100110101011011000001101101101
# 13. 01001101010110110000011011011011
# 14. 10011010101101100000110110110110
# 15. 00110101011011000001101101101101
# 16. 01101010110110000011011011011011
# 17. 11010101101100000110110110110110
# 18. 10101011011000001101101101101101
# 19. 01010110110000011011011011011011
# 20. 10101101100000110110110110110110
# 21. 01011011000001101101101101101101
# 22. 10110110000011011011011011011011
# 23. 01101100000110110110110110110110
# 24. 11011000001101101101101101101101
# 25. 10110000011011011011011011011011
# 26. 01100000110110110110110110110110
# 27. 11000001101101101101101101101101
# 28. 10000011011011011011011011011011
# 29. 00000110110110110110110110110110
# 30. 00001101101101101101101101101101
# 31. 00011011011011011011011011011011
# 32. 00110110110110110110110110110110
