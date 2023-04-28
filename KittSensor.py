import pyaudio

pyaudio_handle = pyaudio.PyAudio()

for i in range(pyaudio_handle.get_device_count()):
    device_info = pyaudio_handle.get_device_info_by_index(i)
    print(i, device_info['name'])

Fs = 48000  # Sampling freq
device_index = device_info[:]  # Chosen device index
stream = pyaudio_handle.open(input_device_index=device_index,
    channels=5,
    format=pyaudio.paInt16,
    rate=Fs,
    input=True)