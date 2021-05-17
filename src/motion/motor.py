import RPi.GPIO as gpio

gpio.setmode( gpio.BCM )

class Motor:
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

    def startPWM( self, duty_cycle ):
        self.pwm.start(duty_cycle)

    def stopPWM( self ):
        self.pwm.stop()

    def moveForward( self ):
        gpio.output( self.in1, 1 )
        gpio.output( self.in2, 0 )

    def moveBack( self ):
        gpio.output( self.in1, 0 )
        gpio.output( self.in2, 1 )

    def stop( self ):
        gpio.output( self.in1, 0 )
        gpio.output( self.in2, 0 )

