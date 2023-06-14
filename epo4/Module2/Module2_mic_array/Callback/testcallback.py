"""
Testing callback mode
"""
import serial.tools.list_ports

from epo4.Module2.Module2_mic_array.Deconvolution import *

# Sampling data
Fs = 48000
Time_recording = 10  # in seconds
N_mic = 5  # number of mics/channels
N = Time_recording * Fs  # number of frames per mic
N_total = N_mic * N  # total number of samples
filename = 'epo4/Module2/Module2_mic_array/Mic-Data/kitt_carrier_2250_bit_3k_ref.txt'

new_frame = np.array([])
data = np.array([])
locations = np.array([])


def recording():
    def callback(in_data, frame_count, time_info, status=0):
        data = np.frombuffer(in_data, dtype='int16').reshape(frame_count, 1)

        print("data test", data)

        # TODO: save date txt

        return (data, pyaudio.paContinue)

    # Create instance of PyAudio
    p = pyaudio.PyAudio()

    # List the index and names of all audio devices visible to PyAudio
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(i, device_info['name'])

    # Automate the correct PyAudio device index
    desired_device_name1 = "Microphone (AudioBox 1818 VSL)"
    desired_device_name2 = "Microphone (2- AudioBox 1818 VS"
    desired_device_name3 = "Microphone (2- AudioBox 1818 VSL)"

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if (device_info["name"] == desired_device_name1 or
                device_info["name"] == desired_device_name2 or
                device_info["name"] == desired_device_name3):
            device_index = i
            break

    input("Device found, starting stream")

    # # Open stream using callback (3)
    # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    #                 channels=wf.getnchannels(),
    #                 rate=wf.getframerate(),
    #                 output=True,
    #                 stream_callback=callback)

    stream = p.open(input_device_index=device_index,
                    channels=5,
                    format=pyaudio.paInt16,
                    rate=Fs,
                    input=True,
                    frames_per_buffer=2048,
                    stream_callback=callback)

    stream.start_stream()

    # try:
    while stream.is_active():
        time.sleep(0.1)
        # TODO: move localization to here
        previous_size = 0  # Initialize the previous size
        trigger_size_data_location = 51000
        data_size = len(data)
        if data_size - previous_size >= trigger_size_data_location:
            data_for_live_loc = data[previous_size:trigger_size_data_location]
            live_locations = localization(data_for_live_loc, xref,
                                          mic_positions_xyz,
                                          Fs, eps, Vsound,
                                          len(xref), location_car,
                                          threshold)
            previous_size = data_size



        localizations = np.append(locations, returned_locations, axis=0)
        print("location test", localizations)


    # Add this line after the loop to print the locations
    # print("Locations:", localizations)

    #
    # except KeyboardInterrupt:
    #     pass

    stream.stop_stream()
    p.terminate()
    return locations


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


def plotting():
    # Plotting the microphone data
    dataTotal = np.loadtxt(f'epo4/Module2/Module2_mic_array/Mic-Data/{filename}.txt')

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
    axs[0].plot(time[:int(Fs * 2)], data0[:int(Fs * 2)], label='Microphone 1')
    axs[1].plot(time[:int(Fs * 2)], data1[:int(Fs * 2)], label='Microphone 2')
    axs[2].plot(time[:int(Fs * 2)], data2[:int(Fs * 2)], label='Microphone 3')
    axs[3].plot(time[:int(Fs * 2)], data3[:int(Fs * 2)], label='Microphone 4')
    axs[4].plot(time[:int(Fs * 2)], data4[:int(Fs * 2)], label='Microphone 5')

    # Set labels and title for each subplot
    for i in range(5):
        axs[i].set_ylabel('Amplitude')
        axs[i].set_title('Microphone ' + str(i + 1))

    # Set labels and title for the entire figure
    # fig.suptitle('Data of the five microphones', ha='center')
    axs[-1].set_xlabel('Time [s]')

    # Adjust spacing between subplots
    plt.tight_layout()

    with open(f'../../../ref_ch3_V1.txt', 'w') as file:
        for sample in data2:
            file.write("%s\n" % sample)
        print("Data stored")

    # Export plot
    # plt.savefig(f'Plots-Report/{filename}_report.svg', format='svg')

    # Display the plot
    plt.show()
    return


def stop_pairing():
    # Close connection
    serial_port.close()
    print("Disconnected\n")
    return


def main():
    start_pairing()
    recording()

    # Change: print the returned car locations
    # car_locations = recording()
    # print("Car locations:", car_locations)

    # serial_port.write(b'A0\n')  # off
    # plotting()
    stop_pairing()
    return


main()
