""" 
ECE 5725 Spring 2021
Final Project

PiDog
Aryaa Pai (avp34) and Krithik Ranjan (kr397)

Robot class to handle movements of the robot. 
""" 

# Import global libraries
import motor
import time

# Pins for left motor
LT_PWM = 16
LT_IN1 = 20
LT_IN2 = 21

# Pins for right motor
RT_PWM = 26
RT_IN1 = 6
RT_IN2 = 5

# Define duty cycle
DUTY_CYCLE_RT = 55.0
DUTY_CYCLE_LT = 60.0

""" 
Robot
Class to interface with both motors together. 

motor_rt: Instance of Motor for right motor
motor_lt: Instance of Motor for left motor
"""
class Robot:
    """ 
    Constructor
    """
    def __init__( self ):
        # Define motors
        self.motor_rt = motor.Motor( RT_PWM, RT_IN1, RT_IN2)
        self.motor_lt = motor.Motor( LT_PWM, LT_IN1, LT_IN2)

        # Start the PWM signals
        self.motor_rt.startPWM(DUTY_CYCLE_RT)
        self.motor_lt.startPWM(DUTY_CYCLE_LT)

    """ 
    forward()
    Function to move the robot forward
    """
    def forward( self ):
        # Move forward 
        self.motor_rt.moveForward()
        self.motor_lt.moveForward()

    """ 
    backward()
    Function to move the robot backward
    """
    def backward( self ):
        # Move back 
        self.motor_rt.moveBack()
        self.motor_lt.moveBack()

    """ 
    rotate()
    Function to rotate the robot in place
    """
    def rotate( self ):
        # Rotate in-place 
        self.motor_rt.moveForward()
        self.motor_lt.moveBack()

    """ 
    turnRight()
    Function to turn the robot right
    """
    def turnRight( self ):
        # Turn right 
        self.motor_lt.moveForward()
        self.motor_rt.stop()

    """ 
    turnLeft()
    Function to turn the robot left
    """
    def turnLeft( self ):
        # Turn left 
        self.motor_rt.moveForward()
        self.motor_lt.stop()

    """ 
    stop()
    Function to stop the robot
    """
    def stop( self ):
        # Stop both motors
        self.motor_rt.stop()
        self.motor_lt.stop()
