import subprocess
import time
import speech_recognition as sr
from record import RecordAudio
import speech

def speak( text ):
    espeak_cmd = 'espeak -a 200 -v mb-en1 -s 150 "' + text + '" --stdout | aplay'
    subprocess.check_output(espeak_cmd, shell=True)

def recognize(rec, mic):
    running = True
    result  = ""
    print("Recognizing...")
    while (running):
        mic.record()
        result = speech.recognize(mic.save())

        if result is not None:
            running = False
    return result

def main():
    # Initialize speech recognition
    rec = sr.Recognizer()
    mic = RecordAudio()
    
    # Introduction
    text = "Simple Choice Task. Please give a command."
    command = recognize(rec, mic)

    print("Result: " + command)
main()
