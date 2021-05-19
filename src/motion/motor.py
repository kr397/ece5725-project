""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Motor class to handle movements of a motor. 
""" 

# Import global library
import RPi.GPIO as gpio

# Configure GPIO
gpio.setmode( gpio.BCM )

""" 
Motor
Class to encapsulate interface with a motor

FREQ: Frequency of the PWM signal
pwm: PWM instance
in1: Input 1
in2: Input 2
"""
class Motor:
    """ 
    Constructor
    """
    def __init__( self, pwm_pin, in1_pin, in2_pin ):  
        # Initialize GPIO pins
        gpio.setup(pwm_pin, gpio.OUT)
        gpio.setup(in1_pin, gpio.OUT)
        gpio.setup(in2_pin, gpio.OUT)
        
        self.FREQ = 50
        self.pwm = gpio.PWM(pwm_pin, self.FREQ)
        self.in1 = in1_pin
        self.in2 = in2_pin

        # Start with both inputs low
        gpio.output(self.in1, 0)
        gpio.output(self.in2, 0)

    """ 
    startPWM(duty_cycle)
    Function to start PWM with input duty cycle
    """
    def startPWM( self, duty_cycle ):
        self.pwm.start(duty_cycle)

    """ 
    stopPWM
    Function to stop PWM signal
    """
    def stopPWM( self ):
        self.pwm.stop()

    """ 
    moveForward()
    Function to move the motor in the forward direction
    """
    def moveForward( self ):
        gpio.output( self.in1, 1 )
        gpio.output( self.in2, 0 )

    """ 
    moveBack()
    Function to move the motor back
    """
    def moveBack( self ):
        gpio.output( self.in1, 0 )
        gpio.output( self.in2, 1 )

    """ 
    stop()
    Function to stop the motor
    """
    def stop( self ):
        gpio.output( self.in1, 0 )
        gpio.output( self.in2, 0 )

