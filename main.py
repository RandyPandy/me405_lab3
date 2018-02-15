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

location = 3000
end = 100

GOING = const (0)
STOPPED = const (1)

def notice_me_senpai():
    ## cereal.open()
    ## cereal.command('k')
    if(state==0):    ## Idle, Wait for Keyboard input
        enc.zero()
        state=1
    else if(state==1):  ## Run the control algortithm
        error = ctr.err_calc(enc.read())
        actuation = ctr.do_work()
        drv.set_duty_cycle(actuation)
        if(error<50)
            state=2
    else if(state==2):  ## Open serial port and read data written
        
    else:
        drv.set_duty_cycle(0)

    error = ctr.err_calc(enc.read())
    actuation = ctr.do_work()
    drv.set_duty_cycle(actuation)
    if(error < 50)
        
    

# =============================================================================

if __name__ == "__main__":

    print ('\033[2JTesting scheduler in cotask.py\n')
    drv = driver.MotorDriver()
    enc = encode.MotorEncoder()
    ctr = controller.MotorController(.04, 7000)   ##Initializes controller with gain=1 and location = 50
    #open cereal port
    ##cereal = cereal.cereal()
    
    
    
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

    task = cotask.Task(notice_me_senpai, name = 'Notice_Me', priority = 1,
                        period = 1000, profile = True, trace = False)

    '''
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
                         period = 1000, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
                         period = 100, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    '''
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

