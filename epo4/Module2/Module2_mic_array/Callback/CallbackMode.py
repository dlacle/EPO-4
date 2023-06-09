import numpy as np
import pyaudio
from epo4.Module2.Module2_mic_array.Deconvolution import localization

Fs = int(48e3)
ref = np.loadtxt('epo4/Module2/Module2_mic_array/ref_sig_V1.8.txt')
filename = 'Callback'
channels = 5  # Update with the appropriate number of channels

data = np.array([])  # Declare data as a global variable


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
                                 input=True,
                                 frames_per_buffer=2048,
                                 stream_callback=callback)
    stream.start_stream()

    # Recording and storing mic data
    N = 10 * Fs  # samples
    samples = stream.read(N)
    data = np.frombuffer(samples, dtype='int16')
    with open(f'epo4/Module2/Module2_mic_array/Mic-Data-Callback/{filename}.txt', 'w') as file:
        for sample in data:
            file.write("%s\n" % sample)
        print("Data stored")

    stream.stop_stream()
    pyaudio_handle.terminate()
    return data


def callback(in_data, frame_count, time_info, status=0):
    global new_frames
    new_frames = np.frombuffer(in_data, dtype='int16').reshape(frame_count, channels)
    global location
    global new_location
    global data  # Access the global data variable
    data = np.append(data, new_frames, axis=0)
    if data.shape[0] > int(96e3):
        data = data[(data.shape[0] - int(96e3)):]

    return in_data, pyaudio.paContinue

