import pyaudio
import wave
import speech_recognition as sr
import time

chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
seconds = 5
filename = 'rec.wav'

p = pyaudio.PyAudio()

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []

for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

stream.stop_stream()
stream.close()

#p.terminate()

print('Finished recording')

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

time.sleep(1)

print("Recognizing")

rec = sr.Recognizer()
audio = sr.AudioFile(filename)

with audio as source:
    rec.adjust_for_ambient_noise(source, duration=1)
    audio = rec.record(source)
    
    try:
        res = rec.recognize_google(audio_data=audio)
        print(res)
    except:
        print("Not found")


### SECOND TIME

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []

for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

stream.stop_stream()
stream.close()

p.terminate()

print('Finished recording')

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()


