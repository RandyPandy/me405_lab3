import pyb
import micropython
import time

'''
Author: Matthew Ng, Eugene Kroop, Yavisht Fitter
Date: January 11, 2018
'''

class MotorDriver:
    ''' Motor Driver Class. Has a function to set duty cycle'''
    def __init__(self):
        '''Creates a motor driver on channel A by initializing GPIO pins and turning the motor off for safety'''
        print('Creating a motor driver')
	##initialize pinA10 to motor enable with output open drain and pull up resistors enabled  
        self.pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_OD, pull=pyb.Pin.PULL_UP, af=-1)
        self.pinA10.low()    

	## initialize B4 to control one terminal to motor with push pull, no pull up resistors, 
        ## alternate function enabled to channel 1     
        self.pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=2)

        ## initialized B5 to control one terminal to motor with push pull, no pull up resistors,
        ## alternate function enabled to channel 2    
        self.pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=2)
        
        self.pinB4.low()    #motor off
        self.pinB5.low()    #motor off

        ## setup timer3 at 20000kHz
        self.tim3 = pyb.Timer(3, freq=20000)    
 
        ## set channel1 to PWM tim3
        self.ch1 = self.tim3.channel(1, pyb.Timer.PWM, pin=self.pinB4)   
 
        ## set channel2 to PWM tim3
        self.ch2 = self.tim3.channel(2, pyb.Timer.PWM, pin=self.pinB5)    

    def set_duty_cycle(self, level):
        '''This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
        cycle of the voltage sent to the motor '''
        self.pinA10.high()
        if level > 0:
            self.ch1.pulse_width_percent(level)    #spin clockwise
            self.ch2.pulse_width_percent(0)   #set low without turning motor off
        else:
            self.ch2.pulse_width_percent(-level)   #spin counterclockwise
            self.ch1.pulse_width_percent(0)   #set low without turning motor off

