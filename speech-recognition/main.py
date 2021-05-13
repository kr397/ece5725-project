import subprocess
import time
import speech_recognition as sr
import RPi.GPIO as gpio

from record import RecordAudio
import speech

LED_PIN = 13

def speak( text ):
    espeak_cmd = 'espeak -a 200 -v mb-en1 -s 150 "' + text + '" --stdout | aplay'
    subprocess.check_output(espeak_cmd, shell=True)

def recognize(rec, mic):
    running = True
    result  = ""
    print("[main] Recognizing...")
    
    gpio.output(LED_PIN, 1)
    subprocess.check_output('echo "1" > ../speechToAnimation.fifo', shell=True)

    mic.record()

    gpio.output(LED_PIN, 0)
    subprocess.check_output('echo "2" > ../speechToAnimation.fifo', shell=True)

    result = speech.recognize(mic.save())
    time.sleep(2)

    return result

def main():
    # Initialize speech recognition
    rec = sr.Recognizer()
    mic = RecordAudio()

    # Set up indicator LED
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_PIN, gpio.OUT)
    
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
        COMMANDS = ['GO', 'BACK', 'RIGHT', 'LEFT', 'QUIT', 'LOOK', 'GOOD']

        if command.upper() in COMMANDS: 
            # Send command to FIFO
            fifo_cmd = 'echo ' + command.upper() + ' > ../speechToHand.fifo'
            subprocess.check_output(fifo_cmd, shell=True)

            # Send to animation FIFO
            fifo_cmd = 'echo ' + command.upper() + ' > ../speechToAnimation.fifo'
            subprocess.check_output(fifo_cmd, shell=True)

        # Stop execution if EXIT
        if command.upper() == 'QUIT':
            running = False
main()
