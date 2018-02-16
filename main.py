# -*- coding: utf-8 -*-
#
## @privatesection - Stuff in this file doesn't need to be Doxygen-ed
#
#  @author jr

import pyb
import micropython
import gc

import cotask
import task_share
import print_task
import busy_task

import time
import utime
import motor_Ng_Kropp_Fitter as driver
import controller_Ng_Kropp_Fitter as controller
import encoder_Ng_Kropp_Fitter as encode

# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)


GOING = const (0)
STOPPED = const (1)

def task1_fun ():
    ''' Sets up the first controller, motor, and encoder'''
    global drv, enc, ctr

    state = STOPPED
    counter = 0

    while True:
        if state == GOING:
            error = ctr.err_calc(enc.read())
            actuation = ctr.do_work()
            drv.set_duty_cycle(actuation)
            ##print_task.put('{}\n'.format(error))
            if abs(error)<150:
                drv.set_duty_cycle(0)
                state = STOPPED
            #print_task.put ('GOING\n')

        elif state == STOPPED:
            enc.zero()
            ctr.set_setpoint(2750)
            #print_task.put ('STOPPED\n')
            state = GOING

        else:
            raise ValueError ('Illegal state for task 1')

        # Periodically check and/or clean up memory
        '''counter += 1
        if counter >= 60:
            counter = 0
            print_task.put (' Memory: {:d}\n'.format (gc.mem_free ()))
        '''
        yield (state)


def task2_fun ():
    ''' Function that implements task 2, a task which is somewhat sillier
    than task 1. '''
    global drv2, enc2, ctr2

    state = STOPPED
    counter = 0

    while True:
        if state == GOING:
            error = ctr2.err_calc(enc2.read())
            actuation = ctr2.do_work()
            drv2.set_duty_cycle(actuation)
            ##print_task.put('{}\n'.format(error2))
            if abs(error)<150:
                drv2.set_duty_cycle(0)
                state = STOPPED
            #print_task.put ('GOING\n')

        elif state == STOPPED:
            enc2.zero()
            ctr2.set_setpoint(2750)
            #print_task.put ('STOPPED\n')
            state = GOING

        else:
            raise ValueError ('Illegal state for task 1')

        # Periodically check and/or clean up memory
        '''counter += 1
        if counter >= 60:
            counter = 0
           ##print_task.put (' Memory: {:d}\n'.format (gc.mem_free ()))
        '''
        yield (state)


# =============================================================================

if __name__ == "__main__":

    drv = driver.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5,3,1,2) #motor enable, pin 1, pin 2
    enc = encode.MotorEncoder(pyb.Pin.board.PB6, pyb.Pin.board.PB7,4,1,2)
    ctr = controller.MotorController(.035, 2750)  

    drv2 = driver.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0, pyb.Pin.board.PA1, 5, 1, 2) #motor enable, pin 1, pin 2
    enc2 = encode.MotorEncoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7,8,1,2) #encoder a, encoder b
    ctr2 = controller.MotorController(0.035, 2750)

    print ('\033[2JTesting scheduler in cotask.py\n')

    # Create a share and some queues to test diagnostic printouts
    share0 = task_share.Share ('i', thread_protect = False, name = "Share_0")
    q0 = task_share.Queue ('B', 6, thread_protect = False, overwrite = False,
                           name = "Queue_0")
    q1 = task_share.Queue ('B', 8, thread_protect = False, overwrite = False,
                           name = "Queue_1")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
                         period = 25, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
                         period = 25, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # A task which prints characters from a queue has automatically been
    # created in print_task.py; it is accessed by print_task.put_bytes()

    # Create a bunch of silly time-wasting busy tasks to test how well the
    # scheduler works when it has a lot to do
    '''
    for tnum in range (10):
        newb = busy_task.BusyTask ()
        bname = 'Busy_' + str (newb.ser_num)
        cotask.task_list.append (cotask.Task (newb.run_fun, name = bname, 
            priority = 0, period = 400 + 30 * tnum, profile = True))
    '''
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is sent through the serial por
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list) + '\n')
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')

