import speech_recognition as sr
rec = sr.Recognizer()

audio = sr.AudioFile('rec.wav')

with audio as source:
    audio = rec.record(source)
    res = rec.recognize_google(audio_data=audio)

    print(res)
