import pyaudio
import numpy as np
import matplotlib.pyplot as plt
# import wave

# Create instance of PyAudio
pyaudio_handle = pyaudio.PyAudio()

# List the index and names of all audio
# devices visible to PyAudio
for i in range(pyaudio_handle.get_device_count()):
    device_info = pyaudio_handle.get_device_info_by_index(i)
    print(i, device_info['name'])


#automate the correct PyAudio device index
desired_device_name = "AudioBo0x 1818 VS"
desired_channels = 1
desired_sample_rate = 48000

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if (device_info["name"] == desired_device_name and
            device_info["maxInputChannels"] >= desired_channels and
            device_info["defaultSampleRate"] >= desired_sample_rate):
        device_index = i
        break

# Initialize the microphone array.
Fs = 48000  # Sampling freq
# device_index = 1  # Chosen device index manual

stream = pyaudio_handle.open(input_device_index=device_index,
                             channels=5,
                             format=pyaudio.paInt16,
                             rate=Fs,
                             input=True)

# recording of N frames
Time_recording = 10      # in seconds
N_mic = 5                # number of mics/channels
N = Time_recording * Fs  # number of frames per mic
N_total = N_mic * N      # total number of samples

samples = stream.read(N)

#######

# w = wave.open(r'C:\Users\ZA\Desktop\Audacity-EPO4\01-Audio Track.wav', 'rb')
# sample_width = w.getsampwidth()
# frame_rate = w.getframerate()
#
# print(sample_width, frame_rate)

#######

# data = np.frombuffer(samples, dtype='int16')
# # data = [0b0000, 0b0001, 0b0010, 0b0011]  # Test data
# with open('data_mics.txt', 'w') as fp:
#     for sample in data:
#         fp.write("%s\n" % sample)
#     print("data stored")

# Data_loaded = open('data_mics.txt', 'r')
# data_mic_loaded = []
# for line in Data_loaded:
#     data_mic_loaded.append(line)
# plt.plot(data)
# plt.show()
# print(data[0])

# for i in range()

# Plotting the microphone data

dataTotal = np.loadtxt('data_mics.txt')

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
fig.suptitle('Data of the five microphones', ha='center')
axs[-1].set_xlabel('Time [s]')

# Adjust spacing between subplots
plt.tight_layout()

# Export plot
plt.savefig('Task1.svg', format='svg')

# Display the plot
plt.show()
