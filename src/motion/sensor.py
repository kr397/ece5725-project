""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Sensor module with class for the HC-SR04 Ultrasonic sensor. 
""" 

# Import global libraries
import RPi.GPIO as gpio
import time

# Define pins for HC-SR04
TRIG_PIN = 19
ECHO_PIN = 12

""" 
Ultrasonic
Class to handle interface with the ultrasonic sensor
""" 
class Ultrasonic:
    """ 
    Constructor
    """
    def __init__(self):
        # Initialize the GPIO pins
        gpio.setup(TRIG_PIN, gpio.OUT)
        gpio.setup(ECHO_PIN, gpio.IN)

    """ 
    distance()
    Function to get one distance reading from the sensor

    Returns: Distance in cm
    """
    def distance(self):
        # Set trigger to LOW for 2 us
        gpio.output(TRIG_PIN, 0)
        time.sleep(0.000002)

        # Set trigger to HIGH for 10 us
        gpio.output(TRIG_PIN, 1)
        time.sleep(0.00001)

        gpio.output(TRIG_PIN, 0)

        # Variables to measure time of pulse
        pulse_start = 0
        pulse_end = 0

        # Measure start and stop time of pulse
        while gpio.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        while gpio.input(ECHO_PIN) == 1:
            pulse_stop = time.time()

        # Calculate distance from the time interval of pulse
        pulse_time = pulse_stop - pulse_start
        # Using sound speed of 34300 cm/s
        dist = ( pulse_time * 34300 ) / 2

        return dist
