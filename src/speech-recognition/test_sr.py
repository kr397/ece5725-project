import subprocess
import time
import speech_recognition as sr
import RPi.GPIO as gpio

from record import RecordAudio
import speech

COMMANDS = {
    'GO': ['GO', 'GHOUL', 'GOOGLE'],
    'BACK': ['BACK', 'MATT'],
    'RIGHT': ['RIGHT', 'GOODNIGHT', 'DID I', 'TODAY'],
    'LEFT': ['LEFT', 'LAST'],
    'GOOD': ['GOOD'],
    'LOOK': ['LOOK'],
    'QUIT': ['QUIT', 'QUICK']
}

def recognize(rec, mic):
    running = True
    result  = ""
    print("[main] Recognizing...")

    mic.record()

    result = speech.recognize(mic.save())
    time.sleep(1)

    return result

def check(cmd):
    for key, val in COMMANDS.items():
        if cmd in val:
            return key
    
    return None

def main():
    # Initialize speech recognition
    rec = sr.Recognizer()
    mic = RecordAudio()

    running = True
    while running:
        # Introduction
        print("[main] Please speak a command")
        command = None
        while command is None:
            command = recognize(rec, mic)

        print("[main] Result: " + command)

        found = check(command.upper())
        if found is not None:
            print("[main] Command found: " + found)

        # Stop execution if EXIT
        # if command.upper() == 'QUIT':
        #     running = False

try:
    main()
except KeyboardInterrupt:
    "[main] Exit"