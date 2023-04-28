import pyaudio

pyaudio_handle = pyaudio.PyAudio()

for i in range(pyaudio_handle.get_device_count()):
    device_info = pyaudio_handle.get_device_info_by_index(i)
    print(i, device_info['name'])
