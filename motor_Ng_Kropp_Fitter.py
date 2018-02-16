import pyb
import micropython
import time

'''
Author: Matthew Ng, Eugene Kroop, Yavisht Fitter
Date: January 11, 2018
'''

class MotorDriver:
    ''' Motor Driver Class. Has a function to set duty cycle'''
    def __init__(self, motor_enable, mc_1, mc_2, timer, channel_1, channel_2):
        '''Creates a motor driver on channel A by initializing GPIO pins and turning the motor off for safety'''
        '''Original motor enable is PA10, motor control 1 is PB4, motor control 2 is PB5'''
        print('Creating a motor driver')
	##initialize pinA10 to motor enable with output open drain and pull up resistors enabled  
        self.enable = pyb.Pin(motor_enable, pyb.Pin.OUT_OD, pull=pyb.Pin.PULL_UP, af=-1)
        self.enable.low()    

	## initialize B4 to control one terminal to motor with push pull, no pull up resistors, 
        ## alternate function enabled to channel 1     
        self.mc1 = pyb.Pin(mc_1, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=2)

        ## initialized B5 to control one terminal to motor with push pull, no pull up resistors,
        ## alternate function enabled to channel 2    
        self.mc2 = pyb.Pin(mc_2, pyb.Pin.AF_PP, pull=pyb.Pin.PULL_NONE, af=2)
        
        self.mc1.low()    #motor off
        self.mc2.low()    #motor off

        ## setup timer3 at 20000kHz
        self.tim = pyb.Timer(timer, freq=20000)    
 
        ## set channel1 to PWM tim
        self.ch1 = self.tim.channel(channel_1, pyb.Timer.PWM, pin=self.mc1)   
 
        ## set channel2 to PWM tim
        self.ch2 = self.tim.channel(channel_2, pyb.Timer.PWM, pin=self.mc2)    

    def set_duty_cycle(self, level):
        '''This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
        cycle of the voltage sent to the motor '''
        self.enable.high()
        if level > 0:
            self.ch1.pulse_width_percent(level)    #spin clockwise
            self.ch2.pulse_width_percent(0)   #set low without turning motor off
        else:
            self.ch2.pulse_width_percent(-level)   #spin counterclockwise
            self.ch1.pulse_width_percent(0)   #set low without turning motor off

