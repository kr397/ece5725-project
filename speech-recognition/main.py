import subprocess
import time
import speech_recognition as sr
import RPi.GPIO as gpio

from record import RecordAudio
import speech

# LED Indicator pin
LED_PIN = 13

# Dictionary to store commands with their variations 
COMMANDS = {
    'GO': ['GO', 'GHOUL', 'GOOGLE', 'COOL'],
    'BACK': ['BACK', 'MATT', 'MAC'],
    'RIGHT': ['RIGHT', 'GOODNIGHT', 'DID I', 'TODAY', 'NIGHT', 'LIGHT'],
    'LEFT': ['LEFT', 'LAST', 'YES'],
    'GOOD': ['GOOD'],
    'LOOK': ['LOOK', 'YOLK'],
    'QUIT': ['QUIT', 'QUICK']
}

# List of no commands 
NO_COMMANDS = ['NONE', 'DONE']

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

def check(cmd):
    for key, val in COMMANDS.items():
        if cmd in val:
            return key
    
    return None

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

        command = command.upper()
        check_cmd = check(command.upper())

        # If in invalid commands, continue
        if command in NO_COMMANDS:
            continue
        
        # Send command to Animation
        if not check_cmd is None:
            print("[main] Command found: " + check_cmd)
            command = check_cmd 
            # Existing command mode
            fifo_cmd = 'echo ' + command + ' > ../speechToAnimation.fifo'
            subprocess.check_output(fifo_cmd, shell=True)
            fifo_cmd = 'echo ' + command + ' >> ../speechToAnimation.log'
            subprocess.check_output(fifo_cmd, shell=True)
        else :
            # New command mode
            subprocess.check_output('echo "NEW" > ../speechToAnimation.fifo', shell=True)
            subprocess.check_output('echo "NEW" >> ../speechToAnimation.log', shell=True)

        # Send command to FIFO
        fifo_cmd = 'echo ' + command + ' > ../speechToHand.fifo'
        subprocess.check_output(fifo_cmd, shell=True)
        fifo_cmd = 'echo ' + command + ' >> ../speechToHand.log'
        subprocess.check_output(fifo_cmd, shell=True)

        # Wait for acknowledgement from hand-detector that new command added
        hand_fifo = open('../handToSpeech.fifo', 'r')
        hand_cmd = hand_fifo.readline()[:-1]
        if not hand_cmd is "DONE" and not hand_cmd is "NONE":
            COMMANDS[hand_cmd] = [hand_cmd]

        # Send acknowledgment to animation 
        subprocess.check_output('echo "DONE" >> ../speechToAnimation.log', shell=True)
        subprocess.check_output('echo "DONE" > ../speechToAnimation.fifo', shell=True)

        # Stop execution if EXIT
        if command == 'QUIT':
            running = False

main()
