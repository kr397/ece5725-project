import RPi.GPIO as gpio
import time
from robot import Robot

# Define states for voice commands
STATE_STOP = 0
STATE_GO = 1
STATE_BACK = 2
STATE_RIGHT = 3
STATE_LEFT = 4

curr_state = STATE_STOP

# Create robot object
piDog = Robot()

# Function to execute any of the states
def runCommand( cmd ):
    if cmd == 'GO':
        piDog.forward()
        return 3
    elif cmd == 'BACK':
        piDog.rotate()
        return 2
    elif cmd == 'LEFT':
        piDog.turnLeft()
        return 1
    elif cmd == 'RIGHT':
        piDog.turnRight()
        return 1
    else:
        piDog.stop()
        return 0

# Main function
def main():
    # Main loop while running
    running = True
    while running:
        # Check for commands (change to FIFO later)
        # cmd = input("Command?: ")

        cmd_fifo = open('../speech_cmd', 'r')
        cmd = cmd_fifo.readline()[:-1]
        print("Command: " + str(cmd))

        # Start the action for the received command and then
        # wait for corresponding time interval before stopping
        dur = runCommand( cmd )

        start_time = time.time()
        while ( time.time() < start_time + dur ):
            # Can check if stop command received and break out
            pass

        # Stop the robot
        piDog.stop()

        # Check exit
        if cmd == 'QUIT':
            running = False

try:
    main()
    gpio.cleanup()
except KeyboardInterrupt:
    gpio.cleanup()
