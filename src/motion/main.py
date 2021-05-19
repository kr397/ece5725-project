""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Main script for the motion module.
Runs continuously to receive commands and move the
robot accordingly.
""" 

# Global Python libraries
import RPi.GPIO as gpio
import time
import subprocess

# Local modules
from robot import Robot
from sensor import Ultrasonic

# Configure GPIO
gpio.setmode(gpio.BCM)

# Define states for voice commands
STATE_STOP = 0
STATE_GO = 1
STATE_BACK = 2
STATE_RIGHT = 3
STATE_LEFT = 4

curr_state = STATE_STOP

# Create robot object
piDog = Robot()

# Create ultrasonic sensor object
sensor = Ultrasonic()
DIST_THRESH = 20.0

"""
runCommand(cmd)
Function to execute all the motion states.

cmd: Input command to decide the motion
Returns: Time duration for different movements
"""
def runCommand(cmd):
    # Condition cases to move the robot forward, rotate
    # turn left, right, or stop depending on the command. 
    if cmd == 'GO':
        piDog.forward()
        return 2.0
    elif cmd == 'BACK':
        piDog.rotate()
        return 2.0
    elif cmd == 'LEFT':
        piDog.turnLeft()
        return 1.5
    elif cmd == 'RIGHT':
        piDog.turnRight()
        return 1.5
    else:
        piDog.stop()
        return 0

# Main function
def main():
    # Main loop while running
    running = True
    while running:
        # Check for input command from hand-detector
        cmd_fifo = open('../handToMotion.fifo', 'r')
        cmd = cmd_fifo.readline()[:-1]
        print("Command: " + str(cmd))

        # Start the action for the received command and then
        # wait for corresponding time interval before stopping
        dur = runCommand( cmd )

        start_time = time.time()
        while ( time.time() < start_time + dur and dur > 0):
            # Can check if about to collide with object and break
            # Wait time of 100ms between two successive reads
            time.sleep(0.0001)
            curr_dist = sensor.distance()
            if curr_dist < DIST_THRESH and cmd == "GO":
                # Only stop motion if GO command
                print("Object detected")
                break

        # Stop the robot once movement done
        piDog.stop()
        print("Command done")

        # Check if exit
        if cmd == 'QUIT':
            running = False
        else:
            # Feedback to hand-detector that motion is done
            subprocess.check_output('echo "DONE" >> ../motionToHand.fifo', shell=True)

if __name__ == "__main__":
    try:
        main()
        gpio.cleanup()
    except KeyboardInterrupt:
        gpio.cleanup()
