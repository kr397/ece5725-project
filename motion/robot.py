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
DUTY_CYCLE = 50.0

class Robot:
    def __init__( self ):
        # Define motors
        self.motor_rt = motor.Motor( RT_PWM, RT_IN1, RT_IN2)
        self.motor_lt = motor.Motor( LT_PWM, LT_IN1, LT_IN2)

        # Start the PWM signals
        self.motor_rt.startPWM(DUTY_CYCLE)
        self.motor_lt.startPWM(DUTY_CYCLE)

    def forward( self ):
        # Move forward 
        self.motor_rt.moveForward()
        self.motor_lt.moveForward()

    def backward( self ):
        # Move back 
        self.motor_rt.moveBack()
        self.motor_lt.moveBack()

    def rotate( self ):
        # Rotate in-place 
        self.motor_rt.moveForward()
        self.motor_lt.moveBack()

    def turnRight( self ):
        # Turn right 
        self.motor_lt.moveForward()
        self.motor_rt.stop()
    
    def turnLeft( self ):
        # Turn left 
        self.motor_rt.moveForward()
        self.motor_lt.stop()

    def stop( self ):
        # Stop both motors
        self.motor_rt.stop()
        self.motor_lt.stop()
