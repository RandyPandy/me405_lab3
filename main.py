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

# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)


GOING = const (0)
STOPPED = const (1)

def task1_fun ():
    ''' Function which runs for Task 1, which toggles twice every second in a
    way which is only slightly silly.  '''

    state = STOPPED
    counter = 0

    while True:
        if state == GOING:
            print_task.put ('GOING\n')
            state = STOPPED

        elif state == STOPPED:
            print_task.put ('STOPPED\n')
            state = GOING

        else:
            raise ValueError ('Illegal state for task 1')

        # Periodically check and/or clean up memory
        counter += 1
        if counter >= 60:
            counter = 0
            print_task.put (' Memory: {:d}\n'.format (gc.mem_free ()))

        yield (state)


def task2_fun ():
    ''' Function that implements task 2, a task which is somewhat sillier
    than task 1. '''

    t2buf = bytearray ('<.>')

    char = ord ('a')

    # Test the speed of two different ways to get text out the serial port
    while True:
        # Put a string into the print queue - this is slower, around 2 ms
#        shares.print_task.put ('<' + chr (char) + '>')

        # Use a bytearray with no memory allocation, faster, around 1 ms
        t2buf[1] = char
        print_task.put_bytes (t2buf)

        yield (0)
        char += 1
        if char > ord ('z'):
            char = ord ('a')


# =============================================================================

if __name__ == "__main__":

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
                         period = 1000, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 2, 
                         period = 100, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # A task which prints characters from a queue has automatically been
    # created in print_task.py; it is accessed by print_task.put_bytes()

    # Create a bunch of silly time-wasting busy tasks to test how well the
    # scheduler works when it has a lot to do
    for tnum in range (10):
        newb = busy_task.BusyTask ()
        bname = 'Busy_' + str (newb.ser_num)
        cotask.task_list.append (cotask.Task (newb.run_fun, name = bname, 
            priority = 0, period = 400 + 30 * tnum, profile = True))

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

