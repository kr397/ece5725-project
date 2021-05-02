import speech_recognition as sr

def recognize( audio ):
    rec = sr.Recognizer()
    audio = sr.AudioFile(audio)

    with audio as source:
        rec.adjust_for_ambient_noise(source, duration=0.5)
        audio = rec.record(source)
   
        try:
            res = rec.recognize_google(audio)
            print('[speech] Found: ' + res)
            return res
        except:
            print('[speech] Not found')
            return None
