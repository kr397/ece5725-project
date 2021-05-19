""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Test script for the motion module.
Runs independently to move the robot based on command recieved
from the terminal. 
""" 

import RPi.GPIO as gpio
import time
import subprocess

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

# Function to execute any of the states
def runCommand( cmd ):
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
        # Check for commands (change to FIFO later)
        cmd = input("Command?: ")

        # Start the action for the received command and then
        # wait for corresponding time interval before stopping
        dur = runCommand( cmd )

        start_time = time.time()
        while ( time.time() < start_time + dur and dur > 0):
            # Can check if about to collide with object and break
            time.sleep(0.0001)
            curr_dist = sensor.distance()
            if curr_dist < DIST_THRESH and cmd == "GO":
                print("Object detected")
                break

        # Stop the robot
        piDog.stop()

        print("Command done")        

        # Check exit
        if cmd == 'QUIT':
            running = False

try:
    main()
    gpio.cleanup()
except KeyboardInterrupt:
    gpio.cleanup()
