import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave

# Create instance of PyAudio
pyaudio_handle = pyaudio.PyAudio()

# List the index and names of all audio
# devices visible to PyAudio
for i in range(pyaudio_handle.get_device_count()):
    device_info = pyaudio_handle.get_device_info_by_index(i)
    print(i, device_info['name'])

# InitializedT the microphone array.
Fs = 48000  # Sampling freq
device_index = 1  # Chosen device index

# stream = pyaudio_handle.open(input_device_index=device_index,
#                              channels=5,
#                              format=pyaudio.paInt16,
#                              rate=Fs,
#                              input=True)

# recording of N frames
Time_recording = 10     # in seconds
N_mic = 5               # number of mics/channels
N = Time_recording * Fs # number of frames per mic
N_total = N_mic * N     # total number of samples

# samples = stream.read(N)

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



# Plot settings
data = np.loadtxt('data_mics.txt')
# data1 = data[0:N_total:5]
time = np.arange(len(data)) / Fs

plt.plot(time, data)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Audio Recording')
plt.show()
