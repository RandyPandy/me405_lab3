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

data = Queue('I', 800)
adc = None

def interrupt(timer):
    global data, adc
    if adc is not None and not data.full():
        data.put(adc.read())

if __name__ == "__main__":

    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.IN)
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    adc = pyb.ADC(pinC0)

    pinC1.low()
    tim1 = pyb.Timer(1, freq=1000, callback=interrupt)
    pinC1.high()

    while True:
        if data.full():
            break

    tim1.callback(None)

    while not data.empty():
        print(data.get()*0.000805)
    pinC1.low()

