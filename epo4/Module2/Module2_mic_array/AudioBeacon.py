"""
Audio beacon and code transmission of Module 2
"""
import time
import serial
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports

# # Sampling data
Fs = 48000
# Time_recording = S  # in seconds
# N_mic = 5  # number of mics/channels
# N = Time_recording * Fs  # number of frames per mic
# N_total = N_mic * N  # total number of samples
# filename_loc = '380x100'
# filename = f'Mic-Data\Mic-Data-V1\kitt_carrier_2250_bit_3k_{filename_loc}'


# Chosen carrier=2250 Hz, bit=3000 Hz, and rep=1250

def start_pairing():
    """
    This function starts the pairing mode to KITT,
    transmission takes place over port 7
    """
    # get port info
    ports = serial.tools.list_ports.comports()
    for i in range(len(ports)):
        print(f"{i} - {ports[i].description}")
    comport = 'COM7'
    # comport = ports[int(input(f"Enter device index: \n"))].device

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
    carrier_frequency = (2250).to_bytes(2, byteorder='big')
    serial_port.write(b'F' + carrier_frequency + b'\n')
    time.sleep(0.1)

    # Bit freq = 2 kHz
    bit_frequency = (3000).to_bytes(2, byteorder='big')
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
    time.sleep(3)
    return


def mic_recording(S):#s
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
    desired_device_name4 = "Microfoon (AudioBox 1818 VSL)"
    desired_device_name5 = "Microfoon (2- AudioBox 1818 VS"
    desired_device_name6 = "Microfoon (2- AudioBox 1818 VSL)"

    for i in range(pyaudio_handle.get_device_count()):
        device_info = pyaudio_handle.get_device_info_by_index(i)
        if (device_info["name"] == desired_device_name1 or
                device_info["name"] == desired_device_name2 or
                device_info["name"] == desired_device_name3 or
                device_info["name"] == desired_device_name4 or
                device_info["name"] == desired_device_name5 or
                device_info["name"] == desired_device_name6):
            device_index = i
            break

    stream = pyaudio_handle.open(input_device_index=device_index,
                                 channels=5,
                                 format=pyaudio.paInt16,
                                 rate=Fs,
                                 input=True)
    Time_recording = S  # in seconds
    N_mic = 5  # number of mics/channels
    N = Time_recording * Fs  # number of frames per mic
    N_total = N_mic * N  # total number of samples

    # Recording and storing mic data
    print('recording')
    samples = stream.read(N)
    print('recording finish')
    data = np.frombuffer(samples, dtype='int16')
    # with open(f'{filename}.txt', 'w') as file:
    #     for sample in data:
    #         file.write("%s\n" % sample)
    #     print("Data stored")
    return data


def plotting():
    # Plotting the microphone data
    dataTotal = np.loadtxt(f'{filename}.txt')

    data0 = dataTotal[0:N_total:5]
    data1 = dataTotal[1:N_total:5]
    data2 = dataTotal[2:N_total:5]
    data3 = dataTotal[3:N_total:5]
    data4 = dataTotal[4:N_total:5]

    # Create an array for time based on the length of the data
    time_total = np.arange(len(dataTotal)) / Fs
    time = np.arange(len(data2)) / Fs

    # Plot Datatotal
    plt.plot(time_total, dataTotal)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Audio Recording')

    # Plot each channel

    # Create subplots for each microphone channel
    fig, axs = plt.subplots(5, 1, figsize=(8, 10))

    # Plot the data for each microphone
    axs[0].plot(time[:int(Fs*2)], data0[:int(Fs*2)], label='Microphone 1')
    axs[1].plot(time[:int(Fs*2)], data1[:int(Fs*2)], label='Microphone 2')
    axs[2].plot(time[:int(Fs*2)], data2[:int(Fs*2)], label='Microphone 3')
    axs[3].plot(time[:int(Fs*2)], data3[:int(Fs*2)], label='Microphone 4')
    axs[4].plot(time[:int(Fs*2)], data4[:int(Fs*2)], label='Microphone 5')

    # Set labels and title for each subplot
    for i in range(5):
        axs[i].set_ylabel('Amplitude')
        axs[i].set_title('Microphone ' + str(i + 1))

    # Set labels and title for the entire figure
    # fig.suptitle('Data of the five microphones', ha='center')
    axs[-1].set_xlabel('Time [s]')

    # Adjust spacing between subplots
    plt.tight_layout()

    # with open(f'../../../ref_ch3_V1.txt', 'w') as file:
    #     for sample in data2:
    #         file.write("%s\n" % sample)
    #     print("Data stored")

    # Export plot
    plt.savefig(f'Plots-Report/{filename_loc}_report.svg', format='svg')

    # Display the plot
    plt.show()
    return



def stop_pairing():
    # Close connection
    serial_port.close()
    print("Disconnected\n")
    return


# def main():
#     start_pairing()
#     mic_recording()
#     serial_port.write(b'A0\n')  # off
#     plotting()
#     stop_pairing()
#     return


# main()
