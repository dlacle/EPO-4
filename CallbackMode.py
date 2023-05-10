import pyaudio

def callback(in_data, frame_count, time_info, status):
    # Do something with the audio data
    processed_data = process_audio(in_data)
    return (processed_data, pyaudio.paContinue)


# Create a PyAudio object
p = pyaudio.PyAudio()

# Open a stream in callback mode
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)
