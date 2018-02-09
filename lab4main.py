# -*- coding: utf-8 -*-
#
## @privatesection - Stuff in this file doesn't need to be Doxygen-ed
#
#  @author jr

import pyb
import micropython
import gc
import utime
import time

import cotask
from task_share import Queue
import print_task
import busy_task
import machine
import os

# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)

data = Queue('I', 900)
adc = None

def interrupt(timer):
    '''
    This is the ISR that is run when the timer runs out
    It won't overflow data. Instead it will stop putting values in the Queue
    '''
    global data, adc
    if adc is not None and not data.full():
        data.put(adc.read())

if __name__ == "__main__":
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.IN) # Setting pin A5 as input to the ADC
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP) # Setting pin A4 as output 
    adc = pyb.ADC(pinC0)

    pinC1.low()
    tim1 = pyb.Timer(1, freq=300, callback=interrupt) #Setting Timer to 1kHz
    pinC1.high()

    while True: # Run until data is full
        if data.full():
            break

    tim1.callback(None) # prevent calling back

    while not data.empty():
        print(data.get()*0.000805) #Convert values to voltage
    pinC1.low()

