import pyaudio
import wave

SAMPLE_FORMAT = pyaudio.paInt16 # 16 bits per sample
FS = 44100 # Sampling rate

class RecordAudio:
    def __init__(s):
        s.chunk = 512  # Record in chunks of 1024 samples
        s.channels = 1
        s.seconds = 5
        s.filename = "output.wav"
        s.frames = [] # Empty array to store frames

        s.p = pyaudio.PyAudio()  # Create an interface to PortAudio

    def record(s):
        print('Recording')
        stream = s.p.open(format=SAMPLE_FORMAT,
                channels=s.channels,
                rate=FS,
                frames_per_buffer=s.chunk,
                input=True)

        # Store data in chunks for 3 seconds
        for i in range(0, int(FS / s.chunk * s.seconds)):
            data = stream.read(s.chunk)
            s.frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        s.p.terminate()

        print('Finished recording')

    def save(s):
        # Save the recorded data as a WAV file
        wf = wave.open(s.filename, 'wb')
        wf.setnchannels(s.channels)
        wf.setsampwidth(s.p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FS)
        wf.writeframes(b''.join(s.frames))
        wf.close()

        return s.filename

