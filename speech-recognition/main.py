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
    print("[main] Recognizing...")
    
    mic.record()
    result = speech.recognize(mic.save())

    return result

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

        # Action commands
        # GO
        # BACK
        # STOP
        # RIGHT
        # LEFT
        # EXIT

        # Send command to FIFO
        fifo_cmd = 'echo ' + command.upper() + ' > ../speechToHand.fifo'
        subprocess.check_output(fifo_cmd, shell=True)

        # Stop execution if EXIT
        if command.upper() == 'QUIT':
            running = False
main()
